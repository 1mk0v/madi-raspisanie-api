from MADI.my_requests import Teachers as teacher_reqs
from MADI.teacher import Teacher
from MADI.main import remove_spaces
from typing import Annotated


from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix='/teacher', tags=['Teachers'])

teachers_req = teacher_reqs()

@router.get('/')
async def get_all_teachers(
# sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
# year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year():
    sem:int,
    year: int
    ):

    """Returns the id and names of teachers in MADI"""

    html = await teachers_req.get(year, sem)
    if len(html) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    for teacher in html:
        if int(teacher['value']) > 0:
            data[teacher['value']] = remove_spaces(teacher.text)

    return data


@router.get('/{id}/schedule/')
async def get_teacher_schedule(id: int,
                               sem: int,
                               year:int):

    """Returns JSON teacher schudule"""

    html = await teachers_req.get_schedule(id, year, sem)

    data = Teacher.get_schedule(html=html)

    return data


@router.get('/{id}/exam/')
async def get_teacher_exam(id: int,
                           sem: int,
                           year: int):

    """Returns JSON exam of teacher by id and year"""

    html = await teachers_req.get_exam(id, year, sem)

    data = Teacher.exam_schedule(html=html)

    return data


# @router.post('/{id}')
# async def add_teacher(id:int):
#     pass