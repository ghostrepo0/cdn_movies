from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Request

from src.core.helper_functions import decode_cookie
from src.core.messages import FilmMessages as msgs  # noqa
from src.models import Film, FilmDetailedResponse, FilmResponse
from src.models.queries import (
    SEARCH_PARAM,
    UUID_PARAM,
    FilterQueryParams,
    PaginationQueryParams,
    SortQueryParams,
)
from src.services.films import FilmService, get_film_service

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=Union[FilmDetailedResponse, FilmResponse],
    summary=msgs.FILMS_ID_GET_SUMMARY,
    description=msgs.FILMS_ID_GET_DESCRIPTION,
    response_description=msgs.FILMS_ID_GET_RESPONSE_DESCR,
)
async def film_details(
    request: Request,
    film_id: str = UUID_PARAM,
    film_service: FilmService = Depends(get_film_service),
) -> Union[FilmDetailedResponse, FilmResponse]:

    user_role = decode_cookie(request.cookies.get("csrf_access_token")).get("role")
    film: Optional[Film] = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.FILM_NOT_FOUND,
        )

    if (not user_role) or (user_role == "unknown"):
        return FilmResponse(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )

    return FilmDetailedResponse(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        type=film.type,
        description=film.description,
        genres=film.genres,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
    )


@router.get(
    "/search/",
    response_model=list[FilmResponse],
    summary=msgs.FILMS_SEARCH_GET_SUMMARY,
    description=msgs.FILMS_SEARCH_GET_DESCRIPTION,
)
async def film_search(
    request: Request,
    query: Optional[str] = SEARCH_PARAM,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponse]:

    _cache_key = str(request.url)

    if sorting.sort_field is None:
        sorting.sort_field = "-imdb_rating"

    films_search_result: list[Optional[Film]] = await film_service.search(
        key=_cache_key,
        query_field=query,
        sort_field=sorting.sort_field,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_order=sorting.sort_order,
    )

    if len(films_search_result) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.FILMS_NOT_FOUND,
        )

    return [
        FilmResponse(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films_search_result
    ]


@router.get(
    "/",
    response_model=list[FilmResponse],
    summary=msgs.FILMS_ALL_GET_SUMMARY,
    description=msgs.FILMS_ALL_GET_DESCRIPTION,
    response_description=msgs.FILMS_ALL_GET_RESPONSE_DESCR,
)
async def film_all(
    request: Request,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    filtering: FilterQueryParams = Depends(FilterQueryParams),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponse]:

    _cache_key = str(request.url)

    if sorting.sort_field is None:
        sorting.sort_field = "-imdb_rating"

    user_role = decode_cookie(request.cookies.get("csrf_access_token")).get("role")

    if (not user_role) or (user_role == "unknown"):
        pagination.page_number = 1
        pagination.page_size = 10

    films_all: list[Film] = await film_service.get_all(
        key=_cache_key,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_field=sorting.sort_field,
        sort_order=sorting.sort_order,
        filter_field=filtering.filter_field,
        filter_value=filtering.filter_value,
    )

    if len(films_all) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.FILMS_NOT_FOUND,
        )

    return [
        FilmResponse(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films_all
    ]
