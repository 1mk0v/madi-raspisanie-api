from database.interfaces.time import DBTime
from database.interfaces.frequency import DBFrequency
from database.interfaces.date import DBDate
from database.interfaces.schedule_type import DBType
from database.interfaces.weekday import DBWeekday
from database.interfaces.auditorium import DBAuditorium
from database.interfaces.discipline import DBDiscipline
from database.models import Response_Message
from MADI.models import Schedule, Time, Date
from typing import List
from fastapi import APIRouter, HTTPException, Body
import datetime

router = APIRouter(prefix='/db', tags=['Database Methods'])

detail = {
    "none":"There NONE value can't storage in DB"
}

#==========================TIME==========================#

@router.get('/time/all')
async def get_time():
    try:
        return await DBTime.get_all()
    except ValueError:
        return HTTPException(404)

@router.post('/time/add')
async def add_time(
    time:Time
):
    if time == None:
        return Response_Message(id=time, detail=detail['none'])
    try:
        res = await DBTime.get_one(
            start=time.start,
            end=time.end
        )
        return Response_Message(id=res['id'], detail='Already add')
    except Exception:
        last_id = await DBTime.add(start=time.start, end=time.end)
        return Response_Message(id=last_id)
        
    
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
        res = await DBFrequency.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')
    except:
        last_id = await DBFrequency.add(value=value)
        return Response_Message(id=last_id)
        
    
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
    date:Date
):
    try:
        new_time = await add_time(time=date.time)
        new_frequency = await add_frequency(date.friequency)
        res = await DBDate.get_one(
            day=date.day,
            frequency_id=new_frequency.id,
            time_id=new_time.id
            )
        return Response_Message(id=res['id'], detail="Already add")
    except Exception as error:
        last_id = await DBDate.add(
                day=date.day,
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
        res = await DBType.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')
    except Exception as error:
        last_id = await DBType.add(value=value)
        return Response_Message(id=last_id)
        

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
        res = await DBWeekday.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')
    except Exception as error:
        last_id = await DBWeekday.add(value=value)
        return Response_Message(id=last_id)

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
        res = await DBAuditorium.get_by_value(value=value)
        return Response_Message(id=res['id'], detail='Already add')
    except:
        last_id = await DBAuditorium.add(value=value)
        return Response_Message(id=last_id)

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
async def add_discipline(value:str | List):

    if type(value) == str:
        value = [value]
    if type(value) == list and len(value) == 0:
        return Response_Message(id=None, detail=detail['none'])
    else:
        for element in value:
            try:
                res = await DBDiscipline.get_by_value(value=element)
                return Response_Message(id=res['id'], detail='Already add')
            except:
                last_id = await DBDiscipline.add(value=element)
                return Response_Message(id=last_id)

@router.delete('/discipline/delete/{id}')
async def delete_discipline(id:int):
    return await DBDiscipline.delete(id=id)

