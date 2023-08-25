from MADI.main import remove_spaces, get_current_year, get_current_sem
from MADI.Requests.requests import Groups as group_req
from MADI.Parsers.groups import Group
from MADI.models import (
    Group as Group_Model,
    Schedule_Group,
    Schedule_Group_Info as Schedule,
    Exam_Group_Info as Exam)
from database.interfaces.group import DBGroups
from database.interfaces.schedule import DBScheduleInfo
from database.models import Response_Message
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Path
from requests import exceptions
router = APIRouter(prefix='/group', tags=['Groups'])

groups_req = group_req()

async def get_group_id(value:str):
    pass

@router.get('/',responses={
    200:{
        "model":List[Group_Model]
        }
    }
)
async def get_groups(
    # year: Annotated[int, Path(ge=19, le=get_current_year()+1)] = get_current_year()
):
    """
        Returns all ID's of groups and their names
    """
    
    try:
        html = await groups_req.get()
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBGroups.get_actual()
        except ValueError:
            raise HTTPException(404)
    
    data = list()
    for element in html:
        data.append(Group_Model(id=element['value'], value=remove_spaces(element.text)))
    return data


@router.get('/{id}/schedule/',responses={
    200:{
        "model":Schedule
        }
    }
)
async def get_group_schedule(
    id:int,
    sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
    year: Annotated[int, Path(ge=19, le=get_current_year()+1)] = get_current_year(),
    name:str = None
):
    """
    Returns JSON schudule of group by id
    """
    try:
        html = await groups_req.get_schedule(id, sem, year, name)
    except (exceptions.ConnectionError, ValueError):
        try:
            group=await DBGroups.get_by_column('id', id)
            schedule = await DBScheduleInfo.get_by_group(id)
            return Schedule(group_info=group[0],
                                  schedule=schedule)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])

    data = Group.schedule(html=html, group=Group_Model(id=id, value=name))
    return data


@router.get('/{id}/exam/',responses={
    200:{
        "model":Exam
        }
    }
)
async def get_group_exams(id:int,
                          sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                          year: Annotated[int, Path(ge=19, le=get_current_year()+1)] = get_current_year(),
                          name:str = None):
    """
    Returns JSON exams of group by id
    """

    try:
        html = await groups_req.get_exam(id,sem, year, name)
    except exceptions.ConnectionError:
        return HTTPException(502)
    except ValueError:
        raise HTTPException(404)
    
    data = Group.exam_schedule(html=html, group=Group_Model(id=id, value=name))
    return data


@router.post('/add')
async def add_group(
    group:Group_Model
):
    if group == None:
        return Response_Message(id=group, detail="The NONE value can't store in DB")
    try:
        res = await DBGroups.get_by_value(value=group.value)
        return Response_Message(id = res["id"], detail="Already Add")
    except:
        last_id = await DBGroups.add(id=group.id, value=group.value)
        return Response_Message(id=last_id)


@router.post('/add/all')
async def add_all_group(
):
    add_res = list()
    groups = await get_groups()
    print(groups)
    for group in groups:
        add_res.append(await add_group(group)
        )
    return add_res

@router.delete('/{id}/delete')
async def delete_group(
    id:int
):
    return await DBGroups.delete(id)
