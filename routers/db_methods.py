from database.interfaces.time import DBTime
from database.interfaces.frequency import DBFrequency
from database.interfaces.date import DBDate
from database.interfaces.schedule_type import DBType
from database.interfaces.weekday import DBWeekday
from database.interfaces.auditorium import DBAuditorium
from database.interfaces.schedule import DBScheduleInfo
from database.interfaces.discipline import DBDiscipline
from .teachers import add_teacher
from .groups import add_group
from database.models import Response_Message
from MADI.models import Date, Time, Schedule
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Body
import datetime

router = APIRouter(prefix='/db', tags=['Database Methods'])

#==========================TIME==========================#

@router.get('/time/all')
async def get_time():
    try:
        return await DBTime.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/time/add')
async def add_time(
    start:Annotated[datetime.time | None, Body()] = None,
    end:Annotated[datetime.time | None, Body()] = None
):
    try:
        last_id = await DBTime.add(start=start, end=end)
        return Response_Message(id=last_id)
    except Exception:
        res = await DBTime.get_one(
            start=start,
            end=end
        )
        return Response_Message(id=res['id'], detail='Already add')
    
@router.delete('/time/delete/{id}')
async def delete_time(id:int):
    return await DBTime.delete(id=id)
    
#=======================FREQUENCY========================#

@router.get('/frequency/all')
async def get_frequency():
    try:
        return await DBFrequency.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/frequency/add')
async def add_frequency(value:str):
    try:
        last_id = await DBFrequency.add(value=value)
        return Response_Message(id=last_id)
    except:
        res = await DBFrequency.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')
    
@router.delete('/frequency/delete/{id}')
async def delete_frequency(id:int):
    return await DBFrequency.delete(id=id)


#==========================DATE==========================#

@router.get('/date/all')
async def get_date():
    try:
        return await DBDate.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/date/add')
async def add_date(
    day:Annotated[str | None, Body()],
    frequency:Annotated[str | None, Body()],
    start_time:Annotated[datetime.time | None, Body()],
    end_time:Annotated[datetime.time | None, Body()],
):
    try:
        new_time = await add_time(start=start_time,end=end_time)
        new_frequency = await add_frequency(frequency)
        res = await DBDate.get_one(
            day=day,
            frequency_id=new_frequency.id,
            time_id=new_time.id
            )
        return Response_Message(id=res['id'], detail="Already add")
    except Exception as error:
        last_id = await DBDate.add(
                day=day,
                frequency_id=new_frequency.id,
                time_id=new_time.id
            )
        return Response_Message(id=last_id)

@router.delete("/date/delete/{id}")
async def delete_date(id:int):
    return await DBDate.delete(id=id)


#==========================TYPE==========================#

@router.get('/type/get')
async def get_type():
    try:
        return await DBType.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/type/add')
async def add_type(value:str):
    try:
        last_id = await DBType.add(value=value)
        return Response_Message(id=last_id)
    except Exception as error:
        print(error)
        res = await DBType.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')

@router.delete('/type/delete/{id}')
async def delete_type(id:int):
    return await DBType.delete(id=id)

#========================WEEKDAY=========================#

@router.get('/weekday/get')
async def get_weekday():
    try:
        return await DBWeekday.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/weekday/add')
async def add_weekday(value:str):
    try:
        last_id = await DBWeekday.add(value=value)
        return Response_Message(id=last_id)
    except Exception as error:
        print("WEEKDAY\n",error)
        res = await DBWeekday.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')

@router.delete('/weekday/delete/{id}')
async def delete_weekday(id:int):
    return await DBWeekday.delete(id=id)

#=======================AUDITORIUM========================#

@router.get('/auditorium/get')
async def get_auditorium():
    try:
        return await DBAuditorium.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/auditorium/add')
async def add_auditorium(value:str):
    try:
        last_id = await DBAuditorium.add(value=value)
        return Response_Message(id=last_id)
    except Exception as error:
        print(error)
        res = await DBAuditorium.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')

@router.delete('/auditorium/delete/{id}')
async def delete_auditorium(id:int):
    return await DBAuditorium.delete(id=id)

#=======================DISCIPLINE========================#

@router.get('/discipline/get')
async def get_discipline():
    try:
        return await DBDiscipline.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/discipline/add')
async def add_discipline(value:str):
    try:
        last_id = await DBDiscipline.add(value=value)
        return Response_Message(id=last_id)
    except Exception as error:
        print(error)
        res = await DBDiscipline.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')

@router.delete('/discipline/delete/{id}')
async def delete_discipline(id:int):
    return await DBDiscipline.delete(id=id)

#=========================SCHEDULE========================#

@router.get('/schedule/get')
async def get_schedule():
    try:
        return await DBScheduleInfo.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/schedule/add')
async def add_schedule(
    weekday:Annotated[str | None, Body()],
    date:Annotated[Date | None, Body()],
    discipline:Annotated[str | None, Body()],
    type:Annotated[str | None, Body()],
    auditorium:Annotated[str | None, Body()]
):
    try:
        weekday_info = await add_weekday(weekday)
        date_info = await add_date(
            day=date.day,
            frequency=date.friequency,
            start_time=date.time.start,
            end_time=date.time.end
        )
        discipline_info = await add_discipline(value = discipline)
        type_info = await add_type(value = type)
        auditorium_info = await add_auditorium(value = auditorium)
        print(weekday_info.id, date_info.id, discipline_info.id, type_info.id, auditorium_info.id)

        last_id = await DBScheduleInfo.add(
            weekday_id=weekday_info.id,
            date_id=date_info.id,
            discipline_id=discipline_info.id,
            type_id=type_info.id,
            auditorium_id=auditorium_info.id
        )
        return Response_Message(id=last_id)
    except Exception as error:
        print(error)

@router.delete('/schedule/delete/{id}')
async def delete_schedule(id:int):
    return await DBScheduleInfo.delete(id=id)