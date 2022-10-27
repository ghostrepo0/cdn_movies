from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from services.app_service import AppService, get_obj_service

from .api_descriptions import info
from .query_parametes import page_parameters
from .response_models import Person

router = APIRouter()


@router.get(
    '/persons',
    response_model=List[Person],
    description=info['person_list']['description'],
    summary=info['person_list']['summary']
)
async def person_list(page: dict = Depends(page_parameters),
                      list_service: AppService = Depends(get_obj_service),
                      ) -> List[Person]:
    persons = await list_service.get_list(size=page['size'],
                                          page=page['page'],
                                          model=Person,
                                          index_name='persons',
                                          )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['person_list']['exception'])
    return persons


@router.get(
    '/persons/search',
    response_model=List[Person],
    description=info['person_search']['description'],
    summary=info['person_search']['summary']
)
async def search_person_list(query: str,
                             page: dict = Depends(page_parameters),
                             search: AppService = Depends(get_obj_service),
                             ) -> List[Person]:
    genres = await search.search(size=page['size'],
                                 page=page['page'],
                                 model=Person,
                                 index_name='persons',
                                 search_query=query,
                                 fields=['full_name']
                                 )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['person_search']['exception'])
    return genres


@router.get(
    '/persons/{person_id}',
    response_model=Person,
    description=info['person_detail']['description'],
    summary=info['person_detail']['summary'],
    response_model_by_alias=False
)
async def person_details(person_id: UUID, service: AppService = Depends(get_obj_service)) -> Person:
    person = await service.get_by_id(obj_id=str(person_id), model=Person, index_name='persons')
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=info['person_detail']['exception'])

    return person
