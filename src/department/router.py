from utils import getListOfEssences
from madi import RaspisanieDepartments
from database.interfaces import Interface as DepartmentDatabaseInterface
from database.schemas import department
from models import Essence as Department, Response
from typing import List
from fastapi import APIRouter, HTTPException, status
from requests import exceptions

router = APIRouter(prefix='/department', tags=['Departments'])

raspisanie_departments = RaspisanieDepartments()
departmentTable = DepartmentDatabaseInterface(model=Department, schema=department)

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
)
async def getDepartments():
    try:
        html = await raspisanie_departments.get()
        return Response(statusCode=200, data=getListOfEssences(html=html))
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data=(await departmentTable.getAll()))
        except ValueError:
            raise HTTPException(404)


@router.post('/add')
async def addDepartment(
    department:Department
):
    try:
        await departmentTable.add(department)
        return Response(statusCode=201, data=department)
    except Exception as error:
        raise HTTPException(500, detail=error.args[0])


@router.delete('/{id}/delete')
async def deleteDepartment(
    id:int
):
    return await departmentTable.delete(id)