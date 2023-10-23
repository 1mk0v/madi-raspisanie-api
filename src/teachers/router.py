from fastapi import APIRouter, HTTPException, Depends
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from madi import RaspisanieTeachers
from models import Response
from database.schemas import teacher
from bridges import madi, Generator
from typing import List
from requests import exceptions


from dependencies import current_sem, current_year

router = APIRouter(prefix='/teacher', tags=['Teachers'])
raspisanie_teachers = RaspisanieTeachers()
teacherTable = AcademicCommunityDatabaseInterface(schema=teacher)

@router.get(
    '/',
)
async def get_all_teachers(
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    try:
        html = await raspisanie_teachers.get(year, sem)
        generator = Generator(madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data=(await teacherTable.getActual()))
        except ValueError:
            return HTTPException(404)
    

@router.post('/add')
async def add_teacher(
    teacher
):
    try:
        return Response(statusCode=201, data=(await teacherTable.add(teacher)))
    except Exception as err:
        raise HTTPException(500, detail=err.args[0])
    

@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await teacherTable.delete(id)
