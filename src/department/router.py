from utils import getListOfEssences
from madi import RaspisanieDepartments
from database.interfaces.base import DBDepartment
from models import Essence as Department, ResponseMessage
from typing import List
from fastapi import APIRouter, HTTPException, status
from requests import exceptions
from dependencies import current_year, current_sem

router = APIRouter(prefix='/department', tags=['Departments'])

raspisanie_departments = RaspisanieDepartments()

@router.get(
        '/',
        summary = "GET actual groups",
        description="Get all actual groups from https://raspisanie.madi.ru/tplan/r/?task=7",
        responses = {
            status.HTTP_200_OK:{
                "model":List[Department],
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
        },
)
async def getDepartments():
    try:
        html = await raspisanie_departments.get()
        return getListOfEssences(html=html)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBDepartment.get_all()
        except ValueError:
            raise HTTPException(404)


@router.post('/add')
async def addDepartment(
    department:Department
):
    if department == None:
        return ResponseMessage(id = department , detail="The NONE value can't store in DB")
    try:
        res = await DBDepartment.get_by_column(column_name="value", column_value=department.value)
        return ResponseMessage(id = res['id'], detail="Already Add")
    except:
        res = await DBDepartment.add(department)
        return ResponseMessage(id = res)


@router.delete('/{id}/delete')
async def deleteDepartment(
    id:int
):
    return await DBDepartment.delete(id)