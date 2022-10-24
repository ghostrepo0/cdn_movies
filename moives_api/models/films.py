from typing import Optional

from src.models._base_model import AbstractModel, FilmGenre
from src.models.genres import Genre
from src.models.persons import Person


class FilmResponse(AbstractModel):
    title: str
    imdb_rating: Optional[float] = None


class Film(FilmResponse):

    type: FilmGenre
    description: Optional[str] = None
    genres: Optional[list[Genre]] = None
    directors: Optional[list[Person]] = None
    actors: Optional[list[Person]] = None
    writers: Optional[list[Person]] = None


class FilmDetailedResponse(Film):
    # пока изменений в модели ответа нет,
    # сделано на будущее
    ...
