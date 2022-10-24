from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request

from src.core.messages import PersonMessages as msgs  # noqa
from src.models import Person, PersonResponse
from src.models.queries import (
    SEARCH_PARAM,
    UUID_PARAM,
    FilterQueryParams,
    PaginationQueryParams,
    SortQueryParams,
)
from src.services.persons import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary=msgs.PERSONS_ID_GET_SUMMARY,
    description=msgs.PERSONS_ID_GET_DESCRIPTION,
    response_description=msgs.PERSONS_ID_GET_RESPONSE_DESCR,
)
async def person_details(
    person_id: str = UUID_PARAM,
    person_service: PersonService = Depends(get_person_service),
) -> PersonResponse:

    person: Optional[Person] = await person_service.get_by_id(person_id)

    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.PERSON_NOT_FOUND,
        )

    return PersonResponse(
        id=person.id,
        name=person.name,
    )


@router.get(
    "/search/",
    response_model=list[PersonResponse],
    summary=msgs.PERSONS_SEARCH_GET_SUMMARY,
    description=msgs.PERSONS_SEARCH_GET_DESCRIPTION,
    response_description=msgs.PERSONS_SEARCH_GET_RESPONSE_DESCR,
)
async def person_search(
    request: Request,
    query: Optional[str] = SEARCH_PARAM,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonResponse]:

    _cache_key = str(request.url)

    persons_search_result: list[Optional[Person]] = await person_service.search(
        key=_cache_key,
        query_field=query,
        sort_field=sorting.sort_field,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_order=sorting.sort_order,
    )

    if len(persons_search_result) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.PERSONS_NOT_FOUND,
        )

    return [
        PersonResponse(
            id=person.id,
            name=person.name,
        )
        for person in persons_search_result
    ]


@router.get(
    "/",
    response_model=list[PersonResponse],
    summary=msgs.PERSONS_ALL_GET_SUMMARY,
    description=msgs.PERSONS_ALL_GET_DESCRIPTION,
    response_description=msgs.PERSONS_ALL_GET_RESPONSE_DESCR,
)
async def person_all(
    request: Request,
    pagination: PaginationQueryParams = Depends(PaginationQueryParams),
    sorting: SortQueryParams = Depends(SortQueryParams),
    filtering: FilterQueryParams = Depends(FilterQueryParams),
    person_service: PersonService = Depends(get_person_service),
) -> list[PersonResponse]:

    _cache_key = str(request.url)

    persons_all: list[Optional[Person]] = await person_service.get_all(
        key=_cache_key,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        sort_field=sorting.sort_field,
        sort_order=sorting.sort_order,
        filter_field=filtering.filter_field,
        filter_value=filtering.filter_value,
    )

    if len(persons_all) < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=msgs.PERSONS_NOT_FOUND,
        )

    return [
        PersonResponse(
            id=person.id,
            name=person.name,
        )
        for person in persons_all
    ]
