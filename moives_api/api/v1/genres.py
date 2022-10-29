from http import HTTPStatus
from typing import Optional

from core.messages import GenreMessages as msgs  # noqa
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from models import Genre, GenreResponse
from models.queries import (
    SEARCH_PARAM,
    UUID_PARAM,
    FilterQueryParams,
    PaginationQueryParams,
    SortQueryParams,
)
from services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    summary=msgs.GENRES_ID_GET_SUMMARY,
    description=msgs.GENRES_ID_GET_DESCRIPTION,
    response_description=msgs.GENRES_ID_GET_RESPONSE_DESCR,
)
async def genre_details(
    genre_id: str = UUID_PARAM,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreResponse:

    genre: Optional[Genre] = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.GENRE_NOT_FOUND,
        )

    return GenreResponse(
        id=genre.id,
        name=genre.name,
    )


@router.get(
    "/search/",
    response_model=list[GenreResponse],
    summary=msgs.GENRES_SEARCH_GET_SUMMARY,
    description=msgs.GENRES_SEARCH_GET_DESCRIPTION,
    response_description=msgs.GENRES_SEARCH_GET_RESPONSE_DESCR,
)
async def genre_search(
    request: Request,
    query: Optional[str] = SEARCH_PARAM,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[GenreResponse]:

    _cache_key = str(request.url)

    genres_search_result: list[Optional[Genre]] = await genre_service.search(
        key=_cache_key,
        query_field=query,
        sort_field=sorting.sort_field,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_order=sorting.sort_order,
    )

    if len(genres_search_result) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.GENRES_NOT_FOUND,
        )

    return [
        GenreResponse(
            id=genre.id,  # type: ignore
            name=genre.name,  # type: ignore
        )
        for genre in genres_search_result
    ]


@router.get(
    "/",
    response_model=list[GenreResponse],
    summary=msgs.GENRES_ALL_GET_SUMMARY,
    description=msgs.GENRES_ALL_GET_DESCRIPTION,
    response_description=msgs.GENRES_ALL_GET_RESPONSE_DESCR,
)
async def genre_all(
    request: Request,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    filtering: FilterQueryParams = Depends(FilterQueryParams),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[GenreResponse]:
    _cache_key = str(request.url)

    genres_all: list[Optional[Genre]] = await genre_service.get_all(
        key=_cache_key,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_field=sorting.sort_field,
        sort_order=sorting.sort_order,
        filter_field=filtering.filter_field,
        filter_value=filtering.filter_value,
    )

    if len(genres_all) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.GENRES_NOT_FOUND,
        )

    return [
        GenreResponse(
            id=genre.id,  # type: ignore
            name=genre.name,  # type: ignore
        )
        for genre in genres_all
    ]
