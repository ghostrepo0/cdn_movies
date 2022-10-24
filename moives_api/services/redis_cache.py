from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from aioredis import Redis
from fastapi import Depends

from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.db.redis import get_redis


class CacheInterface(ABC):
    @abstractmethod
    async def put_to_cache(
        self,
        key: Union[bytes, str, memoryview],
        value: Union[bytes, memoryview, str, int, float],
        *,
        expire_time: int = CACHE_EXPIRE_IN_SECONDS,
    ) -> None:
        ...

    @abstractmethod
    async def get_from_cache(
        self,
        key: Union[bytes, str, memoryview],
    ) -> Optional[Union[bytes, memoryview, str, int, float]]:
        ...


class RedisCache(CacheInterface):
    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def get_from_cache(
        self,
        key: Union[bytes, str, memoryview],
    ) -> Optional[Union[bytes, memoryview, str, int, float]]:

        data = await self.redis.get(key)

        if not data:
            return None

        return data

    async def put_to_cache(
        self,
        key: Union[bytes, str, memoryview],
        value: Union[bytes, memoryview, str, int, float],
        *,
        expire_time: int = CACHE_EXPIRE_IN_SECONDS,
    ) -> None:

        await self.redis.set(
            key,
            value,
            ex=expire_time,
        )


def get_cache(
    cache_connection: Union[Redis, Any] = Depends(get_redis),
) -> CacheInterface:

    if isinstance(cache_connection, Redis):
        return RedisCache(cache_connection)

    raise NotImplementedError(
        "Caching for passed connection type `{0}` is not implemented yet.".format(
            type(cache_connection),
        )
    )
