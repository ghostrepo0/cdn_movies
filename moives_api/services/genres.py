from functools import lru_cache
from typing import Type

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models import Genre
from services._base_interface import ServiceInterface
from services.redis_cache import CacheInterface, get_cache


class GenreService(ServiceInterface):
    @property
    def model(self) -> Type[Genre]:
        return Genre

    @property
    def es_index(self) -> str:
        return "genres"

    @property
    def search_fields(self) -> list[str]:
        return ["name^4", "description"]


@lru_cache()
def get_genre_service(
    cache_connection: CacheInterface = Depends(get_cache),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(
        cache=cache_connection,
        elastic=elastic,
    )
