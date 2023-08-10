from MADI.main import  remove_spaces
from MADI.my_requests import Groups as group_req
from MADI.groups import Group
from MADI.models import Group as Group_Model

from typing import List
from database.database import database
from database.schemas import group
from fastapi import APIRouter, HTTPException, exceptions
from requests import exceptions
router = APIRouter(prefix='/group', tags=['Groups'])

groups_req = group_req()


@router.get('/',
            responses={
                200:{
                    "model":List[Group_Model]
                },
                404:{
                    "model":None #TODO
                }
            })
async def get_groups():

    """
    Returns all ID's of groups and their names
    """
    
    try:
        html = await groups_req.get()
    except exceptions.ConnectionError:
        query = group.select()
        return await database.fetch_all(query)
    except ValueError:
        return HTTPException(404)
    
    data = list()
    for tag in html:
        data.append(Group_Model(id=tag['value'], value=tag.text))
    return data


@router.get('/{id}/schedule/')
async def get_group_schedule(id:int, sem:int = None, year:int = None, name:str = None):

    """
    Returns JSON schudule of group by id
    """

    try:
        html = await groups_req.get_schedule(id, sem, year, name)
    except exceptions.ConnectionError:
        return HTTPException(502)
    except ValueError:
        return HTTPException(404)
    

    data = Group.schedule(html=html, group_name=name)
    return data


@router.get('/{id}/exam/')
async def get_group_exams(id: int, sem:int, year:int, name:str = None):

    """
    Returns JSON exams of group by id
    """

    try:
        html = await groups_req.get_exam(id,sem, year, name)
    except ValueError:
        return HTTPException(404)
    except exceptions.ConnectionError:
        return HTTPException(502)
    
    data = Group.exam_schedule(html=html)
    return data


@router.post('/add')
async def add_group(name:str):
    query = group.insert().values(name=name)
    last_record_id = await database.execute(query)
    return {
        last_record_id:name
    }