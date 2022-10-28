from models._base_model import AbstractModel


class Genre(AbstractModel):
    name: str


class GenreResponse(Genre):
    # пока изменений в модели ответа нет,
    # сделано на будущее
    ...
