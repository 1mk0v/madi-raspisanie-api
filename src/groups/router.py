from madi import RaspisanieGroups
from utils import getListOfEssences
from database.interfaces.group import DBGroups
from database.models import Response_Message
from typing import List
from fastapi import APIRouter, HTTPException, status
from requests import exceptions
from .schemas import Group as GroupModel
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
        return getListOfEssences(html=html, model=GroupModel)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBGroups.get_actual()
        except ValueError:
            raise HTTPException(404)


@router.post(
        '/add',
        summary = "ADD group",
        description="Add one group by thier model",
        responses = {
            status.HTTP_201_CREATED:{
                "model":Response_Message,
                "description": "Created Response",
            }
        },
)
async def add_group(
    group:GroupModel
):
    if group == None:
        return Response_Message(id = group , detail="The NONE value can't store in DB")
    try:
        res = await DBGroups.get(id=group.id, value=group.id)
        return Response_Message(id = res['id'], detail="Already Add")
    except:
        res = await DBGroups.add(group)
        return Response_Message(id = res)


@router.delete(
        '/{id}/delete',
        summary = "DELETE group",
        description="DELETE one group by thier id",
        responses = {
            status.HTTP_201_CREATED:{
                "model":Response_Message,
                "description": "Created Response",
            }
        },
)
async def delete_group(
    id:int
):
    return await DBGroups.delete(id)
