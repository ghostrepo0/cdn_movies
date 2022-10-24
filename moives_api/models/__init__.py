# flake8: noqa
from typing import Union

from src.models.films import Film, FilmDetailedResponse, FilmResponse
from src.models.genres import Genre, GenreResponse
from src.models.persons import Person, PersonFilmWork, PersonResponse
from src.models.queries import (
    PAGE_NUMBER_PARAM,
    PAGE_SIZE_PARAM,
    SEARCH_PARAM,
    UUID_PARAM,
    ESSearchQuery,
)

ModelTypes = Union[Film, Person, Genre]
