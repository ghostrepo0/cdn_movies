# flake8: noqa
from typing import Union

from .films import Film, FilmDetailedResponse, FilmResponse
from .genres import Genre, GenreResponse
from .persons import Person, PersonFilmWork, PersonResponse
from .queries import (
    PAGE_NUMBER_PARAM,
    PAGE_SIZE_PARAM,
    SEARCH_PARAM,
    UUID_PARAM,
    ESSearchQuery,
)

ModelTypes = Union[Film, Person, Genre]
