from functools import lru_cache
from typing import Type

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models import Person
from services._base_interface import ServiceInterface
from services.redis_cache import CacheInterface, get_cache


class PersonService(ServiceInterface):
    @property
    def model(self) -> Type[Person]:
        return Person

    @property
    def es_index(self) -> str:
        return "persons"

    @property
    def search_fields(self) -> list[str]:
        return ["name"]


@lru_cache()
def get_person_service(
    cache_connection: CacheInterface = Depends(get_cache),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(
        cache=cache_connection,
        elastic=elastic,
    )
