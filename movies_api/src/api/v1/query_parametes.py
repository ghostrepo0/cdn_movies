from enum import Enum
from typing import List, Optional
from uuid import UUID

from fastapi import Query


class SortTypes(str, Enum):
    imdb_rating__desc: str = "-imdb_rating"
    imdb_rating__asc: str = "imdb_rating"
    creation_date__desc: str = "-creation_date"
    creation_date__asc: str = "creation_date"


async def filter_parameters(
        genre: UUID = Query(None,
                            description="Фильтр по жанру 3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"),
        actor: UUID = Query(None,
                            description="Фильтр по актеру 7159b605-d8bb-4a8f-ae21-e45f56e16412")
):
    return {"genre": genre, "actor": actor}


async def sort_parameters(
        sort: List[Optional[SortTypes]] = Query(None, description='Сортировка по полю')
):
    """
     Сортировок может быть много, важно соблюсти их порядок,
     не допустить противоречивых, отбросить повторения
    """
    if sort:
        seen = set()
        # Прошу прощения:
        return [s.value for s in sort
                if not (s.value.replace('-', "") in
                        seen or seen.add(s.value.replace('-', "")))]
    return []


async def page_parameters(
        size: Optional[int] = Query(10, le=100, ge=1,  # + 1
                                    description="Сколько объектов вернуть"),
        page: Optional[int] = Query(0, ge=0, le=1000,
                                    description="С какой страницы по порядку начать"),
):
    return {"size": size, "page": page}
