from fastapi import APIRouter, HTTPException
from bridges import Generator, madi
from bridges.institutes_requests import madi as madiRequests
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from models import Community, Response
from database.schemas import group
from requests import exceptions as requests_exc
import exceptions as exc

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
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode=200, data = await groupTable.getActual())
        except exc.NotFoundError as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post(
        '/add',
        summary = "ADD group",
        description="Add one group by thier model"
)
async def add_group(group:Community):
    try:
        await groupTable.add(group)
        return Response(statusCode = 201, data=group)
    except exc.BaseClientException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.delete(
        '/{id}/delete',
        summary = "DELETE group",
        description="DELETE one group by thier id",
)
async def delete_group(
    id:int
):
    return await groupTable.delete(id)