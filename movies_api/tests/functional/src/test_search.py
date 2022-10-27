import json
from http import HTTPStatus

import pytest
from functional.testdata.data import (AllTestData, FilmTestData, GenreTestData,
                                      PersonTestData)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'model, search_query, search_fields',
    [
        (FilmTestData(), "my", "title"),
        (GenreTestData(), "actio", "name"),
        (PersonTestData(), "luca", "full_name")
    ]
)
async def test_search(
        make_get_request,
        redis_client,
        model,
        search_query,
        search_fields
):
    """Проверим, работает ли поиск фильмов/жанров/персон"""
    # отправим запрос приложению
    response = await make_get_request(model.search_route, {"query": search_query})
    assert response.status == HTTPStatus.OK
    redis_key = AllTestData().search_query % (model.index_name, search_query, search_fields,)
    # достаём значение из кэша
    values_from_redis = await redis_client.get(redis_key)
    assert values_from_redis
    # прогоним данные из кэша через pydantic модель
    validated_values_from_redis = [model.list_resp_model(**obj) for obj in json.loads(values_from_redis)]
    validated_values_from_response = [model.list_resp_model(**value) for value in response.body]
    # в кэше должно быть то же, что и вернуло нам приложение
    assert validated_values_from_redis == validated_values_from_response


@pytest.mark.parametrize('size,_from',
                         [
                             (0, 0),
                             (2, -1),
                             (0, -10),
                             ('s', 0),
                             ('aaa', 'aaab')
                         ]
                         )
@pytest.mark.parametrize(
    'model, search_query, search_fields',
    [
        (FilmTestData(), "my", "title"),
        (GenreTestData(), "actio", "name"),
        (PersonTestData(), "luca", "full_name")
    ]
)
async def test_search_with_wrong_params(
        make_get_request,
        redis_client,
        model,
        search_query,
        search_fields,
        size,
        _from
):
    """Проверим, работает ли поиск фильмов/жанров/персон
    С невалидными Query параметрами пагинации"""
    # отправим запрос приложению
    response = await make_get_request(model.list_route, {"size": size, "page": _from})
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    'model, search_query, search_fields',
    [
        (FilmTestData(), "zzzzzz", "title"),
        (GenreTestData(), "zzzzzzz", "name"),
        (PersonTestData(), "zzzzzz", "full_name")
    ]
)
async def test_search_not_found(
        make_get_request,
        redis_client,
        model,
        search_query,
        search_fields
):
    """Проверим, что отвечает приложение если фильмы/жанры/персоны не найдены"""
    # отправим запрос приложению
    response = await make_get_request(model.search_route, {"query": search_query})
    assert response.status == HTTPStatus.NOT_FOUND
    redis_key = AllTestData().search_query % (model.index_name, search_query, search_fields,)
    # достаём значение из кэша
    values_from_redis = await redis_client.get(redis_key)
    assert values_from_redis is None
