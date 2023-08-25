from MADI.Requests.requests import Teachers as teacher_requests
from MADI.models import Teacher as Teacher_model, Schedule_Teacher_Info, Exam_Teacher_Info
from MADI.Parsers.teacher import Teacher
from database.interfaces.teachers import DBTeacher
from database.interfaces.schedule import DBScheduleInfo
from database.models import Response_Message
from MADI.main import remove_spaces, get_current_sem, get_current_year
from typing import Annotated, List
from requests import exceptions
from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix='/teacher', tags=['Teachers'])

teachers_req = teacher_requests()


async def get_teacher_id(value:str):
    pass

@router.get(
    '/',
    responses={
        200:{
                "model":List[Teacher_model]
        }
    }
)
async def get_all_teachers(
    sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
    year: Annotated[int, Path(ge=19, le=get_current_year()+1)] = get_current_year()
):

    """
    Returns the id and names of teachers in MADI
    """

    try:
        html = await teachers_req.get(year, sem)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBTeacher.get_actual()
        except ValueError:
            return HTTPException(404)
    
    data = list()
    for element in html:
        if int(element['value']) > 0:

            data.append(Teacher_model(id=element['value'], value=remove_spaces(element.text)))

    return data


@router.get(
        '/{id}/schedule/',
        responses={
        200:{
                "model":Schedule_Teacher_Info
            }
        }
    )
async def get_teacher_schedule(
    id:int,
    name:str = None,
    sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
    year: Annotated[int, Path(ge=19, le=get_current_year()+1)] = get_current_year()
):

    """Returns JSON teacher schudule"""

    try:
        html = await teachers_req.get_schedule(id, year, sem)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBScheduleInfo.get_by_teacher(id=id)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])
    
    data = Teacher.get_schedule(html=html, teacher=Teacher_model(id=id, name=name))

    return data


@router.get(
        '/{id}/exam/',
        responses={
            200:{
                    "model":Exam_Teacher_Info
                }
        }
    )
async def get_teacher_exam(
    id:int,
    sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
    year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()
):
    """
        Returns JSON exam of teacher by id and year
    """
    try:
        html = await teachers_req.get_exam(id, year, sem)
    except (exceptions.ConnectionError):
        raise HTTPException(502)
    except ValueError:
        raise HTTPException(404)
   

    data = Teacher.exam_schedule(html=html, teacher=Teacher_model(id=id))

    return data


@router.post('/add')
async def add_teacher(
    teacher:Teacher_model
):
    if teacher == None:
        return Response_Message(id=teacher, detail="The NONE value can't store in DB")
    try:
        res = await DBTeacher.get_by_value(value = teacher.value)
        return Response_Message(id = res['id'], detail='Already add')
    except:
        id = await DBTeacher.add(teacher)
        return Response_Message(id = id)

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
