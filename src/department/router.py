from database.interfaces import Interface as DepartmentDatabaseInterface
from bridges import madi, Generator
from bridges.institutes_requests import madi as madiRequests
from database.schemas import department
from models import Essence as Department, Response
from fastapi import APIRouter, HTTPException
from requests import exceptions as requests_exc
import exceptions as exc

router = APIRouter(prefix='/department', tags=['Departments'])

raspisanie_departments = madiRequests.RaspisanieDepartments()
departmentTable = DepartmentDatabaseInterface(model=Department, schema=department)

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
)
async def getDepartments():
    try:
        html = await raspisanie_departments.get()
        generator = Generator(madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode=200, data=(await departmentTable.getAll()))
        except exc.NotFoundError as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)