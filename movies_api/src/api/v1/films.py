from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from services.app_service import AppService, get_obj_service

from .api_descriptions import info
from .query_parametes import (filter_parameters, page_parameters,
                              sort_parameters)
from .response_models import FilmDetail, FilmList

router = APIRouter()


@router.get(
    '/films',
    response_model=List[FilmList],
    description=info['film_list']['description'],
    summary=info['film_list']['summary']
)
async def film_list(sort: List[str] = Depends(sort_parameters),
                    page: dict = Depends(page_parameters),
                    list_service: AppService = Depends(get_obj_service),
                    _filter: dict = Depends(filter_parameters)
                    ) -> List[FilmList]:
    films = await list_service.get_list(size=page['size'],
                                        page=page['page'],
                                        model=FilmList,
                                        index_name='movies',
                                        sort=sort,
                                        filters=_filter
                                        )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['film_list']['exception'])
    return films


@router.get(
    '/films/search',
    response_model=List[FilmList],
    description=info['film_search']['description'],
    summary=info['film_search']['summary'],
)
async def search_film_list(query: str,
                           page: dict = Depends(page_parameters),
                           search: AppService = Depends(get_obj_service),
                           ) -> List[FilmList]:
    films = await search.search(size=page['size'],
                                page=page['page'],
                                model=FilmList,
                                index_name='movies',
                                search_query=query,
                                fields=['title']
                                )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['film_search']['exception'])
    return films


@router.get(
    '/films/{film_id}',
    response_model=FilmDetail,
    description=info['film_detail']['description'],
    summary=info['film_detail']['summary']
)
async def film_details(
        film_id: UUID = Path(None,
                             description='id фильма, например, 2a090dde-f688-46fe-a9f4-b781a985275e'),
        service: AppService = Depends(get_obj_service)) -> FilmDetail:
    film = await service.get_by_id(obj_id=str(film_id), model=FilmDetail, index_name='movies')
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['film_detail']['exception'])

    return film
