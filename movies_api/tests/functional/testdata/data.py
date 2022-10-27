from typing import Type

from pydantic import BaseModel

from api.v1.response_models import FilmDetail, FilmList, Genre, Person


class FilmTestData(BaseModel):
    _id: str = "3d825f60-9fff-4dfe-b294-1a45fa1e115d"
    route_name = 'film'
    index_name: str = "movies"
    detail_route: str = 'films/'
    list_route: str = 'films/'
    search_route: str = 'films/search'
    detail_resp_model: Type[BaseModel] = FilmDetail
    list_resp_model: Type[BaseModel] = FilmList


class GenreTestData(BaseModel):
    _id: str = "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
    route_name = 'genre'
    index_name: str = "genres"
    detail_route: str = 'genres/'
    list_route: str = "genres/"
    search_route: str = 'genres/search'
    detail_resp_model: Type[BaseModel] = Genre
    list_resp_model: Type[BaseModel] = Genre


class PersonTestData(BaseModel):
    _id: str = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    route_name = 'person'
    index_name: str = "persons"
    detail_route: str = 'persons/'
    list_route: str = "persons/"
    search_route: str = 'persons/search'
    detail_resp_model: Type[BaseModel] = Person
    list_resp_model: Type[BaseModel] = Person


class AllTestData(BaseModel):
    get_query: str = "%s::query::{'query': {'match_all': {}}, 'from': 0, 'size': 10}"
    get_query_with_params: str = "%s::query::{'query': {'match_all': {}}, 'from': %s, 'size': %s}"

    search_query: str = "%s::query::{'query': {'multi_match':" \
                        " {'query': '%s', 'fields': ['%s'], 'fuzziness': 'auto'}}," \
                        " 'from': 0, 'size': 10}"
    def_response_size: int = 10

