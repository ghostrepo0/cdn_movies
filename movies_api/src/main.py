import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis

description = "Информация о фильмах, жанрах и людях, участвовавших в создании произведения <br /> " \
              "[Ссылка на репозиторий](https://github.com/dmtnndxr/Async_API_sprint_2) "

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description=description,
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,

)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20
    )
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1', tags=['Фильмы'])
app.include_router(genres.router, prefix='/api/v1', tags=['Жанры'])
app.include_router(persons.router, prefix='/api/v1', tags=['Персоны'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.project_host,
        port=8000,
        reload=True,
    )
