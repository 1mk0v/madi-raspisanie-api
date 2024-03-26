
from bridges import madi, Generator
from bridges.institutes_requests import madi as madiRequests
from database import database, schemas
from models import Essence, Response
from fastapi import APIRouter, HTTPException
from requests import exceptions as requests_exc
from bridges.institutes_requests import exceptions as institutes_requests_exc
import exceptions as exc

router = APIRouter(prefix='/department', tags=['Communities'])

raspisanie_departments = madiRequests.RaspisanieDepartments()
departmentTable = database.DatabaseInterface(table=schemas.Department, engine=database.async_engine)

@router.get(
        '/',
        summary = "GET departments",
        response_model=Response
)
async def getDepartments():
    try:
        raise requests_exc.ConnectionError()
        html = await raspisanie_departments.get()
        generator = Generator(madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (requests_exc.ConnectionError, institutes_requests_exc.EmptyResultError):
        try:
            db_result = (await departmentTable.get()).all()
            data = [Essence.model_validate(row._mapping) for row in db_result]
            return Response(data=data)
        except exc.NotFoundError as error:
            raise HTTPException(error.status_code, detail=error.detail)