import logging

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from asyncpg import connect
from core.config import (
    ELASTIC_CONF,
    MINIO_NODE1,
    MINIO_NODE2,
    POSTGRES_CONF,
    PROJECT_NAME,
    REDIS_CONF,
    SERVICE_CONF,
)
from core.logger import LOGGING
from db import elastic, minio, postgres, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from minio import Minio

app = FastAPI(
    title=PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pool = aioredis.ConnectionPool.from_url(
        f"redis://{REDIS_CONF.host}:{REDIS_CONF.port}",
        max_connections=20,
    )
    redis.redis = aioredis.Redis(connection_pool=pool)
    elastic.es = AsyncElasticsearch(hosts=[f"{ELASTIC_CONF.host}:{ELASTIC_CONF.port}"])
    postgres.pg_conn = await connect(
        user=POSTGRES_CONF.user,
        password=POSTGRES_CONF.password,
        database=POSTGRES_CONF.dbname,
        host=POSTGRES_CONF.host,
        port=POSTGRES_CONF.port,
    )
    minio.minio_client_1 = Minio(
        f"{MINIO_NODE1.host}:{MINIO_NODE1.port}",
        access_key=MINIO_NODE1.access_key,
        secret_key=MINIO_NODE1.secret_key,
        secure=False,
    )
    minio.minio_client_2 = Minio(
        f"{MINIO_NODE2.host}:{MINIO_NODE2.port}",
        access_key=MINIO_NODE2.access_key,
        secret_key=MINIO_NODE2.secret_key,
        secure=False,
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
    await postgres.pg_conn.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SERVICE_CONF.host,
        port=SERVICE_CONF.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
