from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FilmGenre(str, Enum):
    movie = "movie"
    tv_show = "tv_show"


class PersonRole(str, Enum):
    actor = "actor"
    director = "director"
    writer = "writer"


class AbstractModel(BaseModel):
    id: UUID


class PersonFilmWork(AbstractModel):
    name: str


class GenresES(AbstractModel):
    name: str


class PersonsES(PersonFilmWork):
    role: Optional[list[PersonRole]] = None
    film_ids: Optional[list[str]] = None

    class Config:
        use_enum_values = True


class MoviesES(AbstractModel):
    title: str
    imdb_rating: Optional[float] = None
    type: FilmGenre
    description: Optional[str] = None
    genres: Optional[list[GenresES]] = None
    directors: Optional[list[PersonFilmWork]] = None
    actors: Optional[list[PersonFilmWork]] = None
    writers: Optional[list[PersonFilmWork]] = None

    class Config:
        use_enum_values = True
