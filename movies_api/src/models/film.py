from typing import List

from base_model import BaseOrjsonModel


class PersonBase(BaseOrjsonModel):
    id: str
    name: str


class GenreBase(BaseOrjsonModel):
    id: str
    name: str


class Film(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float = None
    description: str = None
    genres: List[GenreBase] = []
    actors: List[PersonBase] = []
    writers: List[PersonBase] = []
    directors: List[PersonBase] = []
    file_path: str = None
    age_limit: int = None
    creation_date: str = None

    # deprecated:
    # actors_names: List[str] = []
    # director: List[str] = []
    # writers_names: List[str] = []
