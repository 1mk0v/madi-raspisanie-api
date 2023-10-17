from fastapi import APIRouter, HTTPException, status
from madi import RaspisanieGroups
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from models import Group, Response
from database.schemas import group
from utils import getListOfEssences

from typing import List
from requests import exceptions
from .schemas import Group as GroupModel

router = APIRouter(prefix='/group', tags=['Groups'])

raspisanie_groups = RaspisanieGroups()
groupTable = AcademicCommunityDatabaseInterface(Group, group)

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
)
async def get_groups():
    try:
        html = await raspisanie_groups.get()
        return getListOfEssences(html=html, model=GroupModel)
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data=(await groupTable.getActual()))
        except ValueError:
            raise HTTPException(404)


@router.post(
        '/add',
        summary = "ADD group",
        description="Add one group by thier model"
)
async def add_group(
    group:GroupModel
):
    try:
        await groupTable.add(group)
        return Response(statusCode = 201, data=group)
    except Exception as error:
        raise HTTPException(500, detail=error.args)


@router.delete(
        '/{id}/delete',
        summary = "DELETE group",
        description="DELETE one group by thier id",
)
async def delete_group(
    id:int
):
    return await groupTable.delete(id)
