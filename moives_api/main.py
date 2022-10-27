import logging

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core.config import ELASTIC_CONF, PROJECT_NAME, REDIS_CONF, SERVICE_CONF
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

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


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


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
