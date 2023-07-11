from fastapi import APIRouter
import sqlalchemy 

from routers import week_days
from .groups import get_groups_id, get_groups
from .teachers import get_all_teachers, get_teacher_id
from .departments import get_departemnts, get_department_groups, get_department_teachers, get_department_auditoriums
from database.database import database
from database.schemas import *
router = APIRouter(prefix='/schedule', tags=['Schedules'])


async def execute(query):
    try:
        await database.execute(query)
    except:
        return


async def find_groups(groups:dict, names=list()):
    val_list = list(groups.values())
    key_list = list(groups.keys())

    data = dict()    

    for name in names:
        try:
            position = val_list.index(name)
            data[key_list[position]] = name
        except:
            continue
    return data    
   
    
async def post_week_days():
    for id in week_days:
        query = week_day.insert().values(id=id, value=week_days[id])
        await execute(query)
    return 'Week days is added!'


async def post_departments():
    groups = await get_groups()
    departments = await get_departemnts()
    for id in departments:

        query = department.insert().values(id=id, name=departments[id])
        await execute(query)

        try:
            this_groups = await find_groups(groups , await get_department_groups(id))
            for i in this_groups:
                query =  group.insert().values(id=i, department_id=id, name=this_groups[i])
                await execute(query)
        except:
            continue

        try:
            this_teachers = await get_department_teachers(id)
            for i in this_teachers:
                query = teacher.insert().values(id=i, department_id=id, name=this_teachers[i])
                await execute(query)
        except:
            continue

        try:
            this_auditoriums = await get_department_auditoriums(id)
            for i in this_auditoriums['auditoriums']:
                print(i)
                query = auditorium.insert().values(departments=id, value=this_auditoriums[i])
                await execute(query)
        except:
            continue

    return "Departments is added"
    

async def post_groups():
    groups = await get_groups()
    for id in groups:
        query = group.insert().values(id=id, name=groups[id], department_id=0)
        await execute(query)
    return "Groups is added!"


async def post_teachers():
    teachers = await get_all_teachers()
    for id in teachers:
        query = teacher.insert().values(id=id, name=teachers[id], department_id=0)
        await execute(query)
    return "Teachers is added!"


@router.post('/')
async def post_schedule():

    """Post schudule of all MADI"""
    
    print(await post_week_days())
    print(await post_departments())
    print(await post_groups())
    print(await post_teachers())

    return {'message':'ok'}