import json
from http import HTTPStatus

import pytest
from functional.testdata.data import (AllTestData, FilmTestData, GenreTestData,
                                      PersonTestData)

pytestmark = [
    pytest.mark.parametrize(
        'model',
        [
            FilmTestData(), GenreTestData(), PersonTestData()
        ]
    ),
    pytest.mark.asyncio
]


async def test_get_list(
        make_get_request,
        redis_client,
        model
):
    """Проверим, работает ли получение фильмов/жанров/персон"""
    # отправим запрос приложению
    response = await make_get_request(model.list_route)
    assert response.status == HTTPStatus.OK
    # достаём значение из кэша
    values_from_redis = await redis_client.get(AllTestData().get_query % (model.index_name,))
    assert values_from_redis
    # прогоним данные из кэша через pydantic модель
    validated_values_from_redis = [model.list_resp_model(**obj) for obj in json.loads(values_from_redis)]
    validated_values_from_response = [model.list_resp_model(**value) for value in response.body]
    # в кэше должно быть то же, что и вернуло нам приложение
    assert validated_values_from_redis == validated_values_from_response
    # проверим кол-во объектов в ответе.
    assert len(validated_values_from_response) == AllTestData().def_response_size


@pytest.mark.parametrize('size,_from',
                         [
                             (3, 0),
                             (2, 3),
                             (1, 10)
                         ]
                         )
async def test_get_list_with_params(
        make_get_request,
        redis_client,
        model,
        size,
        _from
):
    """Проверим, работает ли получение фильмов/жанров/персон
    С Query параметрами пагинации"""
    # отправим запрос приложению
    response = await make_get_request(model.list_route, {"size": size, "page": _from})
    assert response.status == HTTPStatus.OK
    # достаём значение из кэша
    values_from_redis = await redis_client.get(AllTestData().get_query_with_params % (model.index_name, _from, size))
    assert values_from_redis
    # прогоним данные из кэша через pydantic модель
    validated_values_from_redis = [model.list_resp_model(**obj) for obj in json.loads(values_from_redis)]
    validated_values_from_response = [model.list_resp_model(**value) for value in response.body]
    # в кэше должно быть то же, что и вернуло нам приложение
    assert validated_values_from_redis == validated_values_from_response
    # проверим кол-во объектов в ответе.
    assert len(validated_values_from_response) == size


@pytest.mark.parametrize('size,_from',
                         [
                             (0, 0),
                             (2, -1),
                             (0, -10),
                             ('s', 0),
                             ('aaa', 'aaab')
                         ]
                         )
async def test_get_list_with_wrong_params(
        make_get_request,
        redis_client,
        model,
        size,
        _from
):
    """Проверим, работает ли получение фильмов/жанров/персон
    С невалидными Query параметрами пагинации"""
    # отправим запрос приложению
    response = await make_get_request(model.list_route, {"size": size, "page": _from})
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
