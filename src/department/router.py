
from bridges import madi, Generator
from bridges.institutes_requests import madi as madiRequests
from database import database, schemas
from models import Essence
from fastapi import APIRouter, HTTPException
from requests import exceptions as requests_exc
import exceptions as exc
from typing import List

router = APIRouter(prefix='/department', tags=['Departments'])

raspisanie_departments = madiRequests.RaspisanieDepartments()
# departmentTable = DepartmentDatabaseInterface(model=Department, schema=department)

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
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])
    
@router.get(
        '/database',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
)
async def getDepartmentsDB() -> List[Essence]:
    try:
        department = database.DatabaseInterface(schemas.Department, database.async_engine)
        res = (await department.get()).all()
        return [Essence(*row) for row in res]
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])