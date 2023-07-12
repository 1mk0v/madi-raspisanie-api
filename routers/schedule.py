from fastapi import APIRouter
import sqlalchemy 


from routers import week_days
from .groups import get_groups, get_group_schedule
from .teachers import get_all_teachers, get_teacher_id
from .departments import get_departemnts, get_department_groups, get_department_teachers, get_department_auditoriums
from database.database import database
from database.schemas import *
router = APIRouter(prefix='/schedule', tags=['Schedules'])


async def execute(query):
    try:
        return await database.execute(query)
    except:
        # print('already add', query)
        return -1
        


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
        query = week_day.insert().values(id=int(id), value=week_days[id])
        await execute(query)
    return 'Week days is added!'


async def post_departments():
    groups = await get_groups()
    departments = await get_departemnts()
    for id in departments:

        query = department.insert().values(id=int(id), name=departments[id])
        await execute(query)
        
        try:
            this_groups = await find_groups(groups , await get_department_groups(id))
            for i in this_groups:
                query =  group.insert().values(id=int(i), department_id=int(id), name=this_groups[i])
                await execute(query)
        except:
            raise Exception('Add groups', id) 
        
        try:
            this_teachers = await get_department_teachers(id)
            for i in this_teachers:
                query = teacher.insert().values(id=int(i), department_id=int(id), name=this_teachers[i])
                await execute(query)
        except:
            print(f"Can't find teachers of {id} departent")
            # raise Exception('Add teachers', id) 

        try:
            this_auditoriums = await get_department_auditoriums(id)
            for i in this_auditoriums['auditoriums']:
                some_auditoriums = i.split(', ')
                for j in some_auditoriums:
                    query = auditorium.insert().values(department_id=int(id), value=j)
                    await execute(query)
        except:
             print(f"Can't find auditoriums of {id} departent")
            # raise Exception('Add auditoriums', id) 

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


async def post_schedule_groups():
    this_groups = await get_groups()
    for group_id in this_groups:
        print(group_id)
        group_schedules = await get_group_schedule(group_id)
        # query = schedule.insert().value(group_id=group_id)
        # last_id = database.execute(query)
        for week_day in group_schedules['schedule']:
            day_schedules = group_schedules['schedule'][week_day]
            for this_schedule in day_schedules:

                week_id = await get_week_day(week_day)

                time_id:int
                try:
                    time_id = await post_or_get_time(time, this_schedule['time'])
                except:
                    continue
                
                # lesson_id:int
                # try:
                #     lesson_id = await post_or_get_id(lesson, this_schedule['name'])
                # except:
                #     print(this_schedule['name'])
                #     continue
                
                print(week_id, time_id)#, lesson_id, type_id, frequency_id, auditorium_id, teacher_id)
                # type_id:int
                # try:
                #     type_id = await post_or_get_id(schedule_type, this_schedule['type'])
                # except:
                #     continue
                # frequency_id:int
                # try:
                #     frequency_id = await post_or_get_id(frequency, this_schedule['frequency'])
                # except:
                #     continue
                # auditorium_id:int
                # try:
                #     auditorium_id = await post_or_get_id(auditorium, this_schedule['auditorium'])
                # except:
                #     continue
                # teacher_id:int
                # try:
                #     teacher_id = await post_or_get_id(teacher, this_schedule['teacher'])
                # except:
                #     continue

                

async def post_or_get_time(schema, data:str) -> int():
    query = schema.insert().values(value=data)
    id = await execute(query)
    if id == -1:
        query = schema.select().where(schema.c.value == data)
        id = (await database.fetch_one(query))[0]
    return int(id)

async def post_or_get_id(schema, data:str) -> int():
    query = schema.insert().values(value=data)
    id = await execute(query)
    if id == -1:
        query = schema.select().where(schema.value == data)
        id = (await database.fetch_one(query))[0]
    return int(id)


async def get_week_day(local_week_day:str) -> int():
    query = week_day.select().where(week_day.c.value == local_week_day)
    week_id = (await database.fetch_one(query))[0]
    return week_id


@router.post('/')
async def post_schedule():

    """Post schudule of all MADI"""

    # print(await post_week_days())
    # print(await post_departments())
    # print(await post_groups())
    # print(await post_teachers())

    print(await post_schedule_groups())

    return {'message':'ok'}