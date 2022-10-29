from http import HTTPStatus
from typing import Optional, Union

from core.messages import FilmMessages as msgs  # noqa
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from models import Film, FilmDetailedResponse, FilmResponse
from models.queries import (
    SEARCH_PARAM,
    UUID_PARAM,
    FilterQueryParams,
    PaginationQueryParams,
    SortQueryParams,
)
from services.file_loader import DownloadFilm, get_file_download_service
from services.films import FilmService, get_film_service

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=Union[FilmDetailedResponse, FilmResponse],
    summary=msgs.FILMS_ID_GET_SUMMARY,
    description=msgs.FILMS_ID_GET_DESCRIPTION,
    response_description=msgs.FILMS_ID_GET_RESPONSE_DESCR,
)
async def film_details(
    film_id: str = UUID_PARAM,
    film_service: FilmService = Depends(get_film_service),
) -> Union[FilmDetailedResponse, FilmResponse]:

    film: Optional[Film] = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.FILM_NOT_FOUND,
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


@router.get(
    "/download/{film_id}",
)
async def download_film(
    request: Request,
    film_id: str = UUID_PARAM,
    film_download_service: DownloadFilm = Depends(get_file_download_service),
) -> RedirectResponse:

    ip_address = request.client.host

    film_url = await film_download_service.get_download_url(
        film_id,
        ip_address,
    )

    if film_url is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No file for film uploaded",
        )

    return RedirectResponse(film_url)
