from abc import ABC, abstractmethod
from typing import Literal, Optional, Type, Union
from uuid import UUID

import backoff
import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Bool, Match, MultiMatch, Nested

from src.core.config import BACKOFF_CONFIG
from src.core.helper_functions import orjson_dumps
from src.models import ESSearchQuery, ModelTypes
from src.services.redis_cache import CacheInterface


class ServiceInterface(ABC):
    def __init__(
        self,
        cache: CacheInterface,
        elastic: AsyncElasticsearch,
    ) -> None:

        self.cache = cache
        self.elastic = elastic

    @property
    @abstractmethod
    def es_index(self) -> str:
        ...

    @property
    @abstractmethod
    def model(self) -> Type[ModelTypes]:
        ...

    @property
    @abstractmethod
    def search_fields(self) -> list[str]:
        ...

    @property
    def _base_search_obj(self) -> Search:
        return Search(
            using=self.elastic,
        )

    def compose_cache_key(self, **kwargs) -> str:
        if uuid_key := kwargs.get("uuid"):
            return "{0}:{1}".format(
                self.es_index,
                uuid_key,
            )

    async def get_by_id(
        self,
        search_id: Union[str, UUID],
    ) -> Optional[ModelTypes]:

        key = self.compose_cache_key(
            uuid=search_id,
        )

        value = await self._from_cache(
            search_id=key,
        )

        if not value:

            value = await self._from_elastic(
                search_id=search_id,
            )

            if not value:
                return None

            await self._cache_value(
                key=key,
                value=value.json(),
            )

        return value

    async def get_all(
        self,
        key: Optional[str] = None,
        *,
        sort_field: Optional[str] = None,
        filter_field: Optional[str] = None,
        filter_value: Optional[str] = None,
        page_number: int = 1,
        page_size: Optional[int] = None,
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> list[Optional[ModelTypes]]:

        if key:
            result = await self.cache.get_from_cache(
                key=key,
            )
            if result:
                return [self.model(**item) for item in orjson.loads(result)]

        result = await self.search(
            key=key,
            sort_field=sort_field,
            filter_field=filter_field,
            filter_value=filter_value,
            page_number=page_number,
            page_size=page_size,
            sort_order=sort_order,
        )

        if key:
            await self._cache_value(
                key=key,
                value=orjson_dumps(
                    obj=[item.dict() for item in result],
                    default=None,
                ),
            )

        return result

    async def search(
        self,
        key: Optional[str] = None,
        *,
        query_field: Optional[str] = None,
        sort_field: Optional[str] = None,
        filter_field: Optional[str] = None,
        filter_value: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 10,
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> list[Optional[ModelTypes]]:

        search_query_conf = ESSearchQuery(
            query_field=query_field,
            sort_field=sort_field,
            filter_field=filter_field,
            filter_value=filter_value,
            page_number=page_number,
            page_size=page_size,
            sort_order=sort_order,
        )

        if key:
            result = await self.cache.get_from_cache(
                key=key,
            )
            if result:
                return [self.model(**item) for item in orjson.loads(result)]

        try:
            result = await self.elastic.search(
                index=self.es_index, body=self._build_search_body(search_query_conf)
            )
        except NotFoundError:
            return []

        result = [self.model(**doc["_source"]) for doc in result["hits"]["hits"]]

        if key:
            await self._cache_value(
                key=key,
                value=orjson_dumps(
                    obj=[item.dict() for item in result],
                    default=None,
                ),
            )

        return result

    def _build_search_body(self, search_query_conf: ESSearchQuery) -> dict:

        es_search = self._base_search_obj

        if search_query_conf.query_field:
            es_search = es_search.query(
                MultiMatch(
                    query=search_query_conf.query_field,
                    fields=self.search_fields,
                    operator="or",
                    fuzziness="AUTO",
                )
            )

        if sort_field := search_query_conf.sort_field:
            if isinstance(sort_field, str) and sort_field.startswith("-"):
                sort_field = sort_field[1:]

            es_search = es_search.sort(
                {sort_field: {"order": search_query_conf.sort_order}}
            )

        if search_query_conf.filter_field:
            es_search = es_search.query(
                Nested(
                    path=search_query_conf.filter_field,
                    query=Bool(
                        must=[
                            Match(
                                **{
                                    "{0}.id".format(
                                        search_query_conf.filter_field
                                    ): search_query_conf.filter_value,
                                }
                            ),
                        ],
                    ),
                ),
            )

        if (page_size := search_query_conf.page_size) and (
            page_number := search_query_conf.page_number
        ):
            _start = page_size * (page_number - 1)
            _end = _start + page_size
            es_search = es_search[_start:_end]

        return es_search.to_dict()

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def _from_cache(
        self,
        search_id: Union[str, UUID],
    ) -> Optional[ModelTypes]:

        cached_value = await self.cache.get_from_cache(
            key=search_id,
        )

        if cached_value:
            cached_value = orjson.loads(cached_value)
            return self.model(**cached_value)

        return cached_value

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def _cache_value(
        self,
        key: Union[bytes, str, memoryview],
        value: Union[bytes, memoryview, str, int, float, dict, list],
    ) -> None:

        await self.cache.put_to_cache(
            key=key,
            value=value,
        )

    @backoff.on_exception(**BACKOFF_CONFIG)
    async def _from_elastic(
        self,
        search_id: Union[str, UUID],
    ) -> Optional[ModelTypes]:

        try:
            es_result = await self.elastic.get(
                index=self.es_index,
                id=search_id,
            )
        except NotFoundError:
            return None

        return self.model(**es_result["_source"])
