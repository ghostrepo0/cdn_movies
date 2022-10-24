from functools import lru_cache
from typing import Type

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.models import Film
from src.services._base_interface import ServiceInterface
from src.services.redis_cache import CacheInterface, get_cache


class FilmService(ServiceInterface):
    @property
    def model(self) -> Type[Film]:
        return Film

    @property
    def es_index(self) -> str:
        return "movies"

    @property
    def search_fields(self) -> list[str]:
        return ["title^3", "description"]


@lru_cache()
def get_film_service(
    cache_connection: CacheInterface = Depends(get_cache),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(
        cache=cache_connection,
        elastic=elastic,
    )
