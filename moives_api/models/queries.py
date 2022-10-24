from typing import Final, Literal, Optional

from fastapi import Query
from fastapi.params import Query as QueryClass
from pydantic import BaseModel


class ESSearchQuery(BaseModel):

    query_field: Optional[str] = None

    filter_field: Optional[str] = None
    filter_value: Optional[str] = None

    page_number: int = 1
    page_size: int = 10

    sort_field: Optional[str] = None
    sort_order: Optional[Literal["asc", "desc"]] = ("desc",)


PAGE_NUMBER_PARAM: Final[QueryClass] = Query(
    alias="page_number",
    title="Номер страницы",
    default=1,
    ge=1,
    description="Номер страницы для показа",
)
PAGE_SIZE_PARAM: Final[QueryClass] = Query(
    alias="page_size",
    title="Размер страницы",
    default=10,
    ge=1,
    le=100,
    description="Кол-во элементов на странице",
)


class PaginationQueryParams:
    def __init__(
        self,
        page_number: Optional[int] = PAGE_NUMBER_PARAM,
        page_size: Optional[int] = PAGE_SIZE_PARAM,
    ) -> None:
        self.page_number = page_number
        self.page_size = page_size


UUID_PARAM: Final[QueryClass] = Query(
    title="UUID",
    default=None,
    description="Уникальный id объекта для его поиска",
)

SEARCH_PARAM: Final[QueryClass] = Query(
    title="Поиск объекта",
    default=None,
    description="Полнотекстовый поиск объекта по названию",
    example="Star",
)

SORT_FIELD_PARAM: Final[QueryClass] = Query(
    title="Поле сортировки",
    default=None,
    description="Название поля объекта по которому будет производится сортировка",
    example="-imdb_rating",
)
SORT_ORDER_PARAM: Final[QueryClass] = Query(
    title="Порядок сортировки",
    default="desc",
    description="Сортировка по убыванию/возрастанию",
    example="desc",
)


class SortQueryParams:
    def __init__(
        self,
        sort_field: Optional[str] = SORT_FIELD_PARAM,
        sort_order: Optional[Literal["asc", "desc"]] = SORT_ORDER_PARAM,
    ) -> None:
        self.sort_field = sort_field
        self.sort_order = sort_order


FILTER_FIELD_PARAM: Final[QueryClass] = Query(
    title="Поле фильтрации",
    default=None,
    description="Поле по которому будет производится фильтрация",
)
FILTER_VALUE_PARAM: Final[QueryClass] = Query(
    title="Значения фильтрация",
    default=None,
    description="Значение поля по которому будет производится фильтрация",
)


class FilterQueryParams:
    def __init__(
        self,
        filter_field: Optional[str] = FILTER_FIELD_PARAM,
        filter_value: Optional[str] = FILTER_VALUE_PARAM,
    ) -> None:
        self.filter_field = filter_field
        self.filter_value = filter_value
