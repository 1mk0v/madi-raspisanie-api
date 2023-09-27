from database.interfaces.teachers import DBTeacher
from models import ResponseMessage
from utils import remove_garbage, getListOfEssences
from typing import List
from requests import exceptions
from fastapi import APIRouter, HTTPException, status, Depends
from madi import RaspisanieTeachers
from dependencies import current_sem, current_year, get_current_sem, get_current_year
from .schemas import Teacher as TeacherModel

router = APIRouter(prefix='/teacher', tags=['Teachers'])

raspisanie_teachers = RaspisanieTeachers()

@router.get(
    '/',
    responses={
        status.HTTP_200_OK:{
                "model":List[TeacherModel]
        }
    }
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
            return await DBTeacher.get_actual()
        except ValueError:
            return HTTPException(404)
    

@router.post('/add')
async def add_teacher(
    teacher:TeacherModel
):
    if teacher == None:
        return ResponseMessage(id=teacher, detail="The NONE value can't store in DB")
    try:
        res = await DBTeacher.get_by_column(column_name='value',column_value=teacher.value)
        return ResponseMessage(id = res[0]['id'], detail='Already add')
    except Exception as err:
        id = await DBTeacher.add(teacher)
        return ResponseMessage(id = id, detail='Success')
    

@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await DBTeacher.delete(id)
