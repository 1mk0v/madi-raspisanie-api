from database.interfaces.time import DBTime
from database.interfaces.date import DBDate
from database.interfaces import base
from database.interfaces import Interface
from database.models import Response_Message
from models import Time, Date
from typing import List
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/db', tags=['Database Methods'])

detail = {
    "none":"There NONE value can't storage in DB"
}


async def get(instanceOfClass:Interface):
    try:
        return await instanceOfClass.get_all()
    except ValueError:
        return HTTPException(404)
    
async def add(instanceOfClass:Interface, value:str | int | None):
    if value == None:
        return Response_Message(id=value, detail=detail['none'])
    try:
        res = await instanceOfClass.get_by_column(column_name = 'value', column_value = value)
        return Response_Message(id=res[0]['id'], detail='Already add')
    except:
        last_id = await instanceOfClass.add(value = value)
        return Response_Message(id=last_id)
    
async def delete(instanceOfClass:Interface, id:str):
    return await instanceOfClass.delete(id=id)

#==========================TIME==========================#
# @router.post('/time/add')
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
        
#==========================DATE==========================#
async def add_date(
    date:Date
):
    try:
        new_time = await add_time(time=date.time)
        new_frequency = await add(base.DBFrequency, date.friequency)
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

#=======================DISCIPLINE========================#
async def add_discipline(value:str | List):

    if type(value) == str:
        value = [value]
    if type(value) == list and len(value) == 0:
        return Response_Message(id = None, detail = detail['none'])
    else:
        for element in value:
            try:
                res = await base.DBDiscipline.get_by_column(column_name='value', column_value=element)
                return Response_Message(id=res[0].id, detail='Already add')
            except:
                last_id = await base.DBDiscipline.add(value=element)
                return Response_Message(id=last_id)

