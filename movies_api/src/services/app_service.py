import json
from functools import lru_cache
from typing import Any, Dict, List, Optional, Type, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Q, Search
from fastapi import Depends
from pydantic import BaseModel

from core.backoff import backoff
from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from services.abstractions import (AbstractService, AsyncCacheStorage,
                                   FullTextSearch)


class Cache(AsyncCacheStorage):
    def __init__(self, redis: Union[Redis, Any]):
        self.redis = redis

    @backoff
    async def get(self, key: str) -> Optional[Union[List[Dict], Dict]]:
        value = await self.redis.get(key)
        if not value:
            return None
        return json.loads(value)

    @backoff
    async def set(self, key: str, value):
        await self.redis.set(
            key,
            json.dumps(value),
            expire=settings.cache_expire_time
        )


class Database(FullTextSearch):
    def __init__(self, elastic: Union[AsyncElasticsearch, Any]):
        self.elastic = elastic

    @backoff
    async def get(
            self,
            index_name: str,
            _id: Optional[str],
            body: Optional[Dict]
    ) -> Optional[Union[List[Dict], Dict]]:

        if _id:
            try:
                document = await self.elastic.get(index=index_name, id=_id)
            except NotFoundError:
                return None
            return document['_source']

        documents = await self.elastic.search(index=index_name, body=body)
        docs = [document['_source'] for document in documents["hits"]["hits"]]
        return docs

    async def set(self):
        raise NotImplementedError


class QueryConstructor:
    @staticmethod
    async def list_query(
            sort: Optional[List[str]],
            filters: Optional[Dict[str, str]],
            start: int,
            size: int,
    ) -> Dict:

        q = Q()
        if not sort:
            sort = []
        if filters:
            for field_name, uuid in filters.items():
                if uuid:
                    q = q + Q("nested", path=field_name + 's',
                              query=Q("term", **{f'{field_name}s.id': str(uuid)}))

        s = Search().query(q).sort(*sort)[start:size + start]
        return s.to_dict()

    @staticmethod
    async def search_query(
            query: str,
            fields: List[str],
            fuzziness: str,
            start: int,
            size: int
    ) -> Dict:

        if not fields:
            fields = ['*']
        q = Q("multi_match", query=query, fields=fields, fuzziness=fuzziness)
        s = Search().query(q)[start:size + start]
        return s.to_dict()


class StorageManager:
    def __init__(self, cache: Cache, db: Database):
        self.cache = cache
        self.db = db

    async def get_data(
            self,
            index: str,
            key: str,
            _id: str = None,
            body: Dict = None
    ) -> Optional[Union[List, Dict]]:

        data = await self.cache.get(key)
        if not data:
            data = await self.db.get(index, _id, body)
            if not data:
                return None
            await self.cache.set(key, data)

        return data


class AppService(AbstractService):
    def __init__(self, query_maker: Type[QueryConstructor], manager: StorageManager):
        self.query_maker = query_maker
        self.manager = manager

    async def get_by_id(self,
                        obj_id: str,
                        index_name: str,
                        model: Type[BaseModel]
                        ) -> Optional[BaseModel]:

        obj = await self.manager.get_data(
            _id=obj_id,
            key=f"{index_name}::id::{obj_id}",
            index=index_name
        )

        if not obj:
            return None

        return model(**obj)

    async def get_list(self,
                       index_name: str,
                       page: int,
                       size: int,
                       model: Type[BaseModel],
                       sort: List[str] = None,
                       filters: Dict[str, str] = None
                       ) -> Optional[List[BaseModel]]:

        query = await self.query_maker.list_query(
            sort=sort,
            filters=filters,
            start=page,
            size=size
        )

        objects = await self.manager.get_data(
            index=index_name,
            key=f"{index_name}::query::{query}",
            body=query
        )

        if not objects:
            return None
        return [model(**obj) for obj in objects]

    async def search(self,
                     index_name: str,
                     page: int,
                     size: int,
                     search_query: str,
                     model: Type[BaseModel],
                     fields: List[str] = None,
                     fuzziness: str = 'auto'
                     ) -> Optional[List[BaseModel]]:

        query = await self.query_maker.search_query(
            query=search_query,
            fields=fields,
            fuzziness=fuzziness,
            start=page,
            size=size
        )

        objects = await self.manager.get_data(
            index=index_name,
            key=f"{index_name}::query::{query}",
            body=query
        )

        if not objects:
            return None
        return [model(**obj) for obj in objects]


@lru_cache()
def get_obj_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        text_search: FullTextSearch = Depends(get_elastic),
) -> AppService:
    return AppService(
        query_maker=QueryConstructor,
        manager=StorageManager(cache=Cache(cache), db=Database(text_search))
    )
