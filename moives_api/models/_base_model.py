from enum import Enum
from uuid import UUID

import orjson
from pydantic import BaseModel

from src.core.helper_functions import orjson_dumps


class FilmGenre(str, Enum):
    movie = "movie"
    tv_show = "tv_show"


class PersonRole(str, Enum):
    actor = "actor"
    director = "director"
    writer = "writer"


class AbstractModel(BaseModel):

    id: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

        use_enum_values = True
