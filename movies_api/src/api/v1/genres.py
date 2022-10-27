from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from services.app_service import AppService, get_obj_service

from .api_descriptions import info
from .query_parametes import page_parameters
from .response_models import Genre

router = APIRouter()


@router.get(
    '/genres',
    response_model=List[Genre],
    description=info['genre_list']['description'],
    summary=info['genre_list']['summary']
)
async def genre_list(page: dict = Depends(page_parameters),
                     list_service: AppService = Depends(get_obj_service),
                     ) -> List[Genre]:
    genres = await list_service.get_list(size=page['size'],
                                         page=page['page'],
                                         model=Genre,
                                         index_name='genres',
                                         )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['genre_list']['exception'])
    return genres


@router.get(
    '/genres/search',
    response_model=List[Genre],
    description=info['genre_search']['description'],
    summary=info['genre_search']['summary']
)
async def search_genre_list(query: str,
                            page: dict = Depends(page_parameters),
                            search: AppService = Depends(get_obj_service),
                            ) -> List[Genre]:
    genres = await search.search(size=page['size'],
                                 page=page['page'],
                                 model=Genre,
                                 index_name='genres',
                                 search_query=query,
                                 fields=['name']
                                 )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['genre_search']['exception'])
    return genres


@router.get(
    '/genres/{genre_id}',
    response_model=Genre,
    description=info['genre_detail']['description'],
    summary=info['genre_detail']['summary']
)
async def genre_details(genre_id: UUID, service: AppService = Depends(get_obj_service)) -> Genre:
    genre = await service.get_by_id(obj_id=str(genre_id), model=Genre, index_name='genres')
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['genre_detail']['exception'])

    return genre
