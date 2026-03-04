from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.crud import (
    create_vacancy,
    delete_vacancy,
    get_vacancy,
    get_vacancy_by_external_id,
    list_vacancies,
    update_vacancy,
)
from app.schemas import VacancyCreate, VacancyRead, VacancyUpdate


router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/", response_model=List[VacancyRead])
async def list_vacancies_endpoint(
    timetable_mode_name: Optional[str] = None,
    city: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
):
    vacancies = await list_vacancies(
        session,
        timetable_mode_name,
        city,
        page,
        page_size,
    )
    return [VacancyRead.model_validate(v) for v in vacancies]

@router.get("/{vacancy_id}", response_model=VacancyRead)
async def get_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    vacancy = await get_vacancy(session, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return VacancyRead.model_validate(vacancy)


@router.post("/", response_model=VacancyRead, status_code=status.HTTP_201_CREATED)
async def create_vacancy_endpoint(
    payload: VacancyCreate, session: AsyncSession = Depends(get_session)
) -> VacancyRead:
    if payload.external_id is not None:
        existing = await get_vacancy_by_external_id(session, payload.external_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vacancy with external_id already exists"
            )
    vacancy = await create_vacancy(session, payload)
    return  VacancyRead.model_validate(vacancy)


@router.put("/{vacancy_id}", response_model=VacancyRead)
async def update_vacancy_endpoint(
    vacancy_id: int,
    payload: VacancyUpdate,
    session: AsyncSession = Depends(get_session),
) -> VacancyRead:
    vacancy = await get_vacancy(session, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return VacancyRead.model_validate(await update_vacancy(session, vacancy, payload))


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy_endpoint(
    vacancy_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    vacancy = await get_vacancy(session, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await delete_vacancy(session, vacancy)
