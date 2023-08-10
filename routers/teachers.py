from MADI.my_requests import Teachers as teacher_reqs
from MADI.models import Teacher as Teacher_model
from MADI.teacher import Teacher
from MADI.main import remove_spaces
from typing import Annotated, List
from requests import exceptions
from database.database import database
from database.schemas import teacher
from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix='/teacher', tags=['Teachers'])

teachers_req = teacher_reqs()

@router.get('/',
            responses={
                200:{
                    "model":List[Teacher_model]
                },
                404:{
                    "model":None #TODO
                }
            })
async def get_all_teachers(
# sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
# year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year():
    sem:int,
    year: int
    ):

    """
    Returns the id and names of teachers in MADI
    """

    try:
        html = await teachers_req.get(year, sem)
    except exceptions.ConnectionError:
        query = teacher.select()
        return await database.fetch_all(query)
    except ValueError:
        return HTTPException(404)
    
    if len(html) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = list()
    for element in html:
        if int(element['value']) > 0:

            data.append(Teacher_model(id=element['value'], value=remove_spaces(element.text)))

    return data


@router.get('/{id}/schedule/')
async def get_teacher_schedule(id: int,
                               sem: int,
                               year:int):

    """Returns JSON teacher schudule"""

    try:
        html = await teachers_req.get_schedule(id, year, sem)
    except ValueError:
        return HTTPException(404)
    except exceptions.ConnectionError:
        return HTTPException(502)
    
    data = Teacher.get_schedule(html=html)

    return data


@router.get('/{id}/exam/')
async def get_teacher_exam(id: int,
                           sem: int,
                           year: int):

    """
    Returns JSON exam of teacher by id and year
    """

    try:
        html = await teachers_req.get_exam(id, year, sem)
    except ValueError:
        return HTTPException(404)
    except exceptions.ConnectionError:
        return HTTPException(502)

    data = Teacher.exam_schedule(html=html)

    return data


@router.post('/add')
async def add_teacher(name:str):
    query = teacher.insert().values(name=name)
    last_record_id = await database.execute(query)
    return {
        last_record_id:name
    }