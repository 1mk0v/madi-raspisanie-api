from database.interfaces.schedule import DBScheduleInfo
from database.models import Response_Message
from other.db_methods import (
    add_date,
    add_weekday,
    add_discipline,
    add_type,
    add_auditorium)
from groups.router import add_group, get_group_schedule, get_groups
from teachers.router import add_teacher
from fastapi import APIRouter, HTTPException
from .schemas import Schedule

router = APIRouter(prefix='/schedule', tags=['Schedule'])

@router.get('/')
async def get_schedule():
    try:
        return await DBScheduleInfo.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/add')
async def add_schedule(schedule:Schedule):

    weekday_info = await add_weekday(schedule.weekday)
    date_info = await add_date(schedule.date)
    discipline_info = await add_discipline(value = schedule.discipline)
    type_info = await add_type(value = schedule.type)
    auditorium_info = await add_auditorium(value = schedule.auditorium)
    teacher_info = await add_teacher(teacher=schedule.teacher)
    group_info = await add_group(group=schedule.group)
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


@router.post('/group/{id}/add')
async def add_by_group_schedule(
    id:int,
    name:str
):
    response_list = list()
    schedule_info = await get_group_schedule(id=id, name=name)
    schedule = schedule_info.schedule
    for weekday in schedule:
        for lesson in schedule[weekday]:
            response_list.append(await add_schedule(
                weekday=weekday,
                teacher=lesson.teacher,
                group=schedule_info.group_info,
                schedule=Schedule(
                    date=lesson.date,
                    discipline=lesson.discipline,
                    type=lesson.type,
                    auditorium=lesson.auditorium
                )
            ))
    return response_list


@router.post('/group/add/all')
async def add_all_groups_schedule():
    data = await get_groups()
    print(data)
    for element in data:
        print('START ADD SCHEDULE FOR GROUP', element)
        try:
            await add_by_group_schedule(id=element.id, name=element.value)
        except:
            continue
        print('END ADD SCHEDULE')

@router.delete('/delete/{id}')
async def delete_schedule(id:int):
    return await DBScheduleInfo.delete(id=id)