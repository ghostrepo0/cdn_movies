from dataclasses import dataclass
from typing import Dict, Optional

import aiohttp
import pytest
from aioredis import Redis, create_redis_pool
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import settings


@dataclass
class HTTPResponse:
    body: Dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture  # убрал здесь скоуп, т.к. евент луп закрывался
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[Dict] = None) -> HTTPResponse:
        params = params or {}
        url = settings.service_url + settings.api_url + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="function")
async def redis_client() -> Redis:
    pool = await create_redis_pool((settings.redis_host, settings.redis_port))
    await pool.flushall()
    yield pool
    await pool.flushall()
    pool.close()
    await pool.wait_closed()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=settings.es_host)
    yield client
    await client.close()

