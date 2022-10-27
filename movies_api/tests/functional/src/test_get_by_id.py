import json
import uuid
from http import HTTPStatus

import pytest
from functional.testdata.data import (FilmTestData, GenreTestData,
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


async def test_get_by_id(
        make_get_request,
        redis_client,
        model
):
    """Проверим, работает ли получение информации о фильме/жанре/персоне по id """
    # отправим запрос приложению
    response = await make_get_request(model.detail_route + model._id)
    assert response.status == HTTPStatus.OK
    # достаём значение из кэша
    value = await redis_client.get(f"{model.index_name}::id::{model._id}")
    # прогоним данные из кэша через pydantic модель
    validated_value = model.detail_resp_model.parse_raw(value)
    # в кэше должно быть то же, что и вернуло нам приложение
    assert json.loads(validated_value.json()) == response.body


async def test_get_by_wrong_id(
        make_get_request,
        redis_client,
        model
):
    """Проверим получение информации о фильме/жанре/персоне по неправильному id"""
    # получим случайный id
    _id = str(uuid.uuid1())
    # отправим запрос приложению
    response = await make_get_request(model.detail_route + _id)
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body == {"detail": f"{model.route_name} not found"}
    # достаём значение из кэша
    value = await redis_client.get(_id)
    # кэшироваться не должно
    assert value is None


@pytest.mark.parametrize('_id', ('1', 's'))
async def test_get_by_invalid_id(
        make_get_request,
        redis_client,
        model,
        _id

):
    """Проверим получение информации о фильме/жанре/персоне по некорректному типу id"""
    # отправим запрос приложению
    response = await make_get_request(model.detail_route + _id)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body == {"detail": [{"loc": ["path", f"{model.route_name}_id"],
                                         "msg": "value is not a valid uuid",
                                         "type": "type_error.uuid"}]}
    # достаём значение из кэша
    value = await redis_client.get(_id)
    # кэшироваться не должно
    assert value is None
