from MADI.models import Date, Schedule
from database.interfaces.schedule import DBScheduleInfo
from database.models import Response_Message
from routers.db_methods import (
    add_date,
    add_weekday,
    add_discipline,
    add_type,
    add_auditorium,
    add_teacher,
    add_group)

from database.schemas import schedule
from fastapi import APIRouter, HTTPException, Body
from typing import Annotated

router = APIRouter(prefix='/schedule', tags=['Schedule'])


@router.get('/')
async def get_schedule():
    try:
        return await DBScheduleInfo.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/schedule/add')
async def add_schedule(
    weekday:Annotated[str | None, Body()],
    teacher:Annotated[str | None, Body()],
    group:Annotated[str | None, Body()],
    schedule:Schedule
):
    weekday_info = await add_weekday(weekday)
    date_info = await add_date(
        day=schedule.date.day,
        frequency=schedule.date.friequency,
        start_time=schedule.date.time.start,
        end_time=schedule.date.time.end
    )
    discipline_info = await add_discipline(value = schedule.discipline)
    type_info = await add_type(value = schedule.type)
    auditorium_info = await add_auditorium(value = schedule.auditorium)
    teacher_info = await add_teacher(name = teacher)
    group_info = await add_group(name = group)
    last_id = await DBScheduleInfo.add(
        weekday_id=weekday_info.id,
        date_id=date_info.id,
        discipline_id=discipline_info.id,
        type_id=type_info.id,
        auditorium_id=auditorium_info.id,
        teacher_id = teacher_info.id,
        group_id = group_info.id
    )
    return Response_Message(id=last_id)

@router.delete('/delete/{id}')
async def delete_schedule(id:int):
    return await DBScheduleInfo.delete(id=id)