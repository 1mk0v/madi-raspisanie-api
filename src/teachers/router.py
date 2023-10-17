from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from models import Teacher, Response
from database.schemas import teacher
from utils import getListOfEssences
from typing import List
from requests import exceptions
from fastapi import APIRouter, HTTPException, status, Depends
from madi import RaspisanieTeachers
from dependencies import current_sem, current_year
from .schemas import Teacher as TeacherModel

router = APIRouter(prefix='/teacher', tags=['Teachers'])
raspisanie_teachers = RaspisanieTeachers()
teacherTable = AcademicCommunityDatabaseInterface(Teacher, teacher)


@router.get(
    '/',
)
async def get_all_teachers(
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    try:
        html = await raspisanie_teachers.get(year, sem)
        return getListOfEssences(html=html, model=TeacherModel)
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data=(await teacherTable.getActual()))
        except ValueError:
            return HTTPException(404)
    

@router.post('/add')
async def add_teacher(
    teacher:TeacherModel
):
    try:
        await teacherTable.add(teacher)
        return Response(statusCode=201, data=teacher)
    except Exception as err:
        raise HTTPException(500, detail=err.args[0])
    

@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await teacherTable.delete(id)
