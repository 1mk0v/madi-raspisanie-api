from MADI.Requests.requests import Teachers as teacher_requests
from MADI.models import Teacher as Teacher_model
from MADI.Parsers.teacher import Teacher
from database.interfaces.teachers import DBTeacher
from database.models import Response_Message
from MADI.main import remove_spaces
from typing import Annotated, List
from requests import exceptions
from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix='/teacher', tags=['Teachers'])

teachers_req = teacher_requests()

@router.get(
    '/',
    responses={
        200:{
                "model":List[Teacher_model]
        }
    }
)
async def get_all_teachers(
# sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
# year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year():
    sem:int,
    year: int
):

    """
    Returns the id and names of teachers in MADI
    """

    #TODO - сократить
    try:
        html = await teachers_req.get(year, sem)
    except (exceptions.ConnectionError, ValueError):
        try:
            return await DBTeacher.get_all()
        except ValueError:
            return HTTPException(404)
    
    data = list()
    for element in html:
        if int(element['value']) > 0:

            data.append(Teacher_model(id=element['value'], value=remove_spaces(element.text)))

    return data


@router.get('/{id}/schedule/')
async def get_teacher_schedule(
    id:int,
    sem:int,
    year:int
):

    """Returns JSON teacher schudule"""

    try:
        html = await teachers_req.get_schedule(id, year, sem)
    except exceptions.ConnectionError:
        return  HTTPException(502)
    except ValueError:
        raise HTTPException(404)
    
    data = Teacher.get_schedule(html=html)

    return data


@router.get('/{id}/exam/')
async def get_teacher_exam(
    id:int,
    sem:int,
    year:int
):

    """
    Returns JSON exam of teacher by id and year
    """

    try:
        html = await teachers_req.get_exam(id, year, sem)
    except exceptions.ConnectionError:
        return HTTPException(502)
    except ValueError:
        raise HTTPException(404)
   

    data = Teacher.exam_schedule(html=html)

    return data


@router.post('/add')
async def add_teacher(
    name:str,
    id:int = None
):
    try:
        last_id = await DBTeacher.add(id=id, value=name)
        return Response_Message(id=last_id)
    except:
        res = await DBTeacher.get_by_value(value=name)
        return Response_Message(id=res['id'], detail='Already add')
    

@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await DBTeacher.delete(id)
