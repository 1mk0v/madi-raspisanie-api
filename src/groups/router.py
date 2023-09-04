from utils import remove_garbage
from madi import RaspisanieGroups
from database.interfaces.group import DBGroups
from database.interfaces.schedule import DBScheduleInfo
from database.models import Response_Message
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from requests import exceptions
from .schemas import Group as GroupModel, Schedule, Exam
from .utils import parse_exam, parse_schedule
from dependencies import current_year, current_sem 
router = APIRouter(prefix='/group', tags=['Groups'])

raspisanie_groups = RaspisanieGroups()

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
        responses = {
            status.HTTP_200_OK:{
                "model":List[GroupModel],
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
        },
)
async def get_groups():
    try:
        html = await raspisanie_groups.get()
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBGroups.get_actual()
        except ValueError:
            raise HTTPException(404)
    
    data = list()
    for element in html:
        data.append(GroupModel(id=element['value'], value=remove_garbage(element.text)))
    return data


@router.get(
        '/{id}/schedule/',
        summary = "GET group schedule",
        description="By default get actual schedule for any group, but you can get old schedule",
        responses={
            status.HTTP_200_OK:{
                "model":Schedule,
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
    }
)
async def get_group_schedule(
    id:int,
    name:str = None,
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    """
    Returns JSON schudule of group by id
    """
    try:
        html = await raspisanie_groups.get_schedule(id, sem, year, name)
    except (exceptions.ConnectionError, ValueError):
        try:
            group=await DBGroups.get_by_column('id', id)
            schedule = await DBScheduleInfo.get_by_group(id)
            return Schedule(group_info = group[0], schedule = schedule)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])

    data = parse_schedule(html=html, group=GroupModel(id=id, value=name))
    return data


@router.get(
        '/{id}/exam/',
        summary = "GET group exams",
        description="By default get actual exam for any group, but you can get old exams",
        responses={
            status.HTTP_200_OK:{
                "model":Exam,
                "description":"OK Response"
            },
            status.HTTP_404_NOT_FOUND:{
                "description":"Response if there is no internet connection and no records in the database"
            }
        }
)
async def get_group_exams(
    id:int,
    sem = Depends(current_sem),
    year = Depends(current_year),
    name:str = None,
):
    try:
        html = await raspisanie_groups.get_exam(id,sem,year,name)
    except (exceptions.ConnectionError, ValueError):
        try:
            raise ValueError
        except ValueError:
            raise HTTPException(404)
    
    data = parse_exam(html=html, group=GroupModel(id=id, value=name))
    return data


@router.post('/add')
async def add_group(
    group:GroupModel
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
