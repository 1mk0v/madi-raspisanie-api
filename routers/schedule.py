from MADI.models import Date
from database.schemas import schedule
from .db_methods import add_schedule
from fastapi import APIRouter, HTTPException, Body
from typing import Annotated

router = APIRouter(prefix='/schedule', tags=['Schedule'])

@router.post('/group/{id}')
async def add_group_schedule(
    group_id:Annotated[int | None, Body()],
    weekday:Annotated[str | None, Body()],
    date:Annotated[Date | None, Body()],
    discipline:Annotated[str | None, Body()],
    type:Annotated[str | None, Body()],
    auditorium:Annotated[str | None, Body()]
):  
    added_schedule = await add_schedule(
            weekday=weekday,
            date=date,
            discipline=discipline,
            auditorium=auditorium,
            type=type
        )
    try:
        pass
    except Exception as error:
        print(error)
    

@router.post('/exam/group/{id}')
async def add_group_exam_schedule(
    group_id:int
):
    pass

@router.post('/teacher/{id}')
async def add_teacher_schedule(
    teacher_id:int
):
    pass

@router.post('/exam/teacher/{id}')
async def add_teacher_exam_schedule(
    teacher_id:int
):
    pass
