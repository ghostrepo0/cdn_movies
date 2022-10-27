from typing import Optional

from models._base_model import AbstractModel, PersonRole


class Person(AbstractModel):

    name: str


class PersonResponse(Person):
    # пока изменений в модели ответа нет,
    # сделано на будущее
    ...


class PersonFilmWork(Person):

    role: Optional[list[PersonRole]] = None
    film_ids: Optional[list[str]] = None
