from fastapi import APIRouter, HTTPException
from bridges import Generator, madi
from bridges.institutes_requests import madi as madiRequests
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from models import Community, Response
from database.schemas import group
from requests import exceptions

router = APIRouter(prefix='/group', tags=['Groups'])

raspisanieGroups = madiRequests.RaspisanieGroups()
groupTable = AcademicCommunityDatabaseInterface(schema=group)

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
)
async def get_groups():
    try:
        html = await raspisanieGroups.get()
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data = await groupTable.getActual())
        except ValueError:
            raise HTTPException(404)


@router.post(
        '/add',
        summary = "ADD group",
        description="Add one group by thier model"
)
async def add_group(group:Community):
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
