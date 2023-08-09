from MADI.main import  remove_spaces
from MADI.my_requests import Groups as group_req
from MADI.groups import Group

from database.database import database
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/group', tags=['Groups'])

groups_req = group_req()


@router.get('/')
async def get_groups():

    """
    Returns all ID's of groups and their names
    """
    data = dict()
    try:
        html = await groups_req.get()
    except Exception as error:
        return HTTPException(404, detail=error.args[0])
    
    for tag in html:
        data[tag['value']] = remove_spaces(tag.text)
    return data


@router.get('/{id}/schedule/')
async def get_group_schedule(id:int, sem:int = None, year:int = None, name:str = None):

    """
    Returns JSON schudule of group by id
    """

    try:
        html = await groups_req.get_schedule(id, sem, year, name)
    except Exception as error:
        return HTTPException(404, detail=error.args[0])
    
    data = Group.schedule(html=html, group_name=name)
    return data


@router.get('/{id}/exam/')
async def get_group_exams(id: int, sem:int, year:int, name:str = None):

    """
    Returns JSON exams of group by id
    """
    try:
        html = await groups_req.get_exam(id,sem, year, name)
    except Exception as error:
        return HTTPException(404, detail=error.args[0])
    
    data = Group.exam_schedule(html=html)
    return data