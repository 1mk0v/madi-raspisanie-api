from MADI.main import  remove_spaces
from MADI.my_requests import Groups as group_req
from MADI.groups import Group
from MADI.models import Group as Group_Model
from database.interfaces.group import DB_Groups
import time
from typing import List
from fastapi import APIRouter, HTTPException, exceptions
from requests import exceptions
router = APIRouter(prefix='/group', tags=['Groups'])

groups_req = group_req()

async def generator():
    html = await groups_req.get()
    for element in html:
        yield {'id':element['value'], 'name':remove_spaces(element.text)}

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
        names = generator()
    except exceptions.ConnectionError:
        return await DB_Groups.get_all()
    except ValueError:
        return HTTPException(404)
    
    data = list()
    async for item in names:
        data.append(Group_Model(id=item['id'], value=item['name']))
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
    return await DB_Groups.add(name)


@router.post('/add-all')
async def add_all_groups():
    groups = list()
    names = generator()
    async for i in names:
        groups.append({'name':i})
    return await DB_Groups.add_list(groups)


@router.delete('/delete/{id}')
async def delete_group(id:int):
    return await DB_Groups.delete(id)
    