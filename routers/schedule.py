from database.interfaces.time import DBTime
from database.interfaces.frequency import DBFrequency
from database.interfaces.date import DBDate, Date
from database.models import Response_Message
from sqlalchemy.exc import IntegrityError
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
        if res == None:
            res = await DBDate.add(
                day=day,
                frequency_id=new_frequency.id,
                time_id=new_time.id
            )
        return res
    except Exception as error:
        print(error)

@router.delete("/date/delete/{id}")
async def delete_date(id:int):
    return await DBDate.delete(id=id)


#==========================TYPE==========================#

@router.get('/type/get')
async def get_type():
    pass

@router.post('/type/add')
async def add_type():
    pass

@router.delete('/type/delete/{id}')
async def delete_type():
    pass

#========================================================#