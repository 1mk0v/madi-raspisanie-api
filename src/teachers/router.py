from database.interfaces.teachers import DBTeacher
from database.interfaces.schedule import DBScheduleInfo
from models import ResponseMessage
from utils import remove_garbage
from typing import List
from requests import exceptions
from fastapi import APIRouter, HTTPException, status, Depends
from madi import RaspisanieTeachers
from dependencies import current_sem, current_year
from .schemas import Teacher as TeacherModel, Schedule, Exam
from .parse import parse_schedule, parse_exam

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

    """
    Returns the id and names of teachers in MADI
    """

    try:
        html = await raspisanie_teachers.get(year, sem)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBTeacher.get_actual()
        except ValueError:
            return HTTPException(404)
    
    data = list()
    for element in html:
        if int(element['value']) > 0:
            data.append(TeacherModel(id=element['value'], value=remove_garbage(element.text)))
    return data


@router.get(
        '/{id}/schedule/',
        responses={
        status.HTTP_200_OK:{
                "model":Schedule
            }
        }
    )
async def get_teacher_schedule(
    id:int,
    name:str = None,
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    try:
        html = await raspisanie_teachers.get_schedule(id, year, sem)
    except (exceptions.ConnectionError, ValueError):
        try:
            teacher = TeacherModel(id=id, value=name)
            schedule = await DBScheduleInfo.get_by_teacher(id=id)
            return Schedule(teacher=teacher, schedule = schedule)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])
    data = parse_schedule(html=html, teacher=TeacherModel(id=id, value=name))
    return data


@router.get(
        '/{id}/exam/',
        responses={
            status.HTTP_200_OK:{
                    "model":Exam
            }
        }
    )
async def get_teacher_exam(
    id:int,
    name:str = None,
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    """
        Returns JSON exam of teacher by id and year
    """
    try:
        html = await raspisanie_teachers.get_exam(id, year, sem)
    except (exceptions.ConnectionError):
        raise HTTPException(502)
    except ValueError:
        raise HTTPException(404)

    data = parse_exam(html=html, teacher=TeacherModel(id=id, value=name))

    return data


@router.post('/add')
async def add_teacher(
    teacher:TeacherModel
):
    if teacher == None:
        return ResponseMessage(id=teacher, detail="The NONE value can't store in DB")
    try:
        res = await DBTeacher.get_by_value(value = teacher.value)
        return ResponseMessage(id = res['id'], detail='Already add')
    except:
        id = await DBTeacher.add(teacher)
        return ResponseMessage(id = id, detail='Success')


@router.post('/add/all')
async def add_all_teachers():
    response_list = list()
    res = await get_all_teachers()
    for teacher in res:
        res = await add_teacher(teacher)
        response_list.append(res)
    return response_list


@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await DBTeacher.delete(id)
