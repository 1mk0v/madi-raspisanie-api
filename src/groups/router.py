from fastapi import APIRouter, HTTPException
from bridges import Generator, madi
from bridges.institutes_requests import madi as madiRequests
from models import Community, Response, ResponseWithCommunity
from database import database, schemas
from requests import exceptions as requests_exc
from bridges.institutes_requests import exceptions as institutes_requests_exc
import exceptions as exc

router = APIRouter(prefix='/group', tags=['Groups'])

raspisanieGroups = madiRequests.RaspisanieGroups()
groupTable = database.DatabaseInterface(table=schemas.Group, engine=database.async_engine)

@router.get(
        '/',
        summary = "GET actual groups",
        response_model=ResponseWithCommunity
)
async def get_groups():
    try:
        html = await raspisanieGroups.get()
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (requests_exc.ConnectionError, institutes_requests_exc.EmptyResultError) as error:
        try:
            db_result = (await groupTable.get()).all()
            data = [Community.model_validate(row._mapping) for row in db_result]
            return Response(data=data)
        except exc.NotFoundError as error:
            raise HTTPException(error.status_code, detail=error.detail)