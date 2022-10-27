from typing import List

from models.base_model import BaseOrjsonModel


class PersonBase(BaseOrjsonModel):
    id: str
    name: str


class Person(BaseOrjsonModel):
    id: str
    full_name: str


class Genre(BaseOrjsonModel):
    id: str
    name: str


class FilmDetail(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None
    description: str = None
    genres: List[Genre] = []
    actors: List[PersonBase] = []
    writers: List[PersonBase] = []
    directors: List[PersonBase] = []


class FilmList(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None
