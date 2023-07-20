from routers import request_url
from routers import get_current_year, get_current_sem

import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Teacher, remove_garbage, remove_spaces, set_selectors
from typing import Annotated


from fastapi import APIRouter, HTTPException, Path
router = APIRouter(prefix='/teacher', tags=['Teachers'])


async def get_teacher_id(name: str = None, names=list()) -> dict():
    """Return ID of teacher"""

    all_teachers: dict = await get_all_teachers()

    val_list = list(all_teachers.values())
    key_list = list(all_teachers.keys())

    data = dict()

    if len(names) == 0 and name == None:
        raise Exception()

    names.append(name)

    for name in names:
        try:
            position = val_list.index(name)
            data[key_list[position]] = name
        except:
            continue

    if len(data) == 0:
        raise HTTPException(404, detail='Not Found')

    return data


@router.get('/')
async def get_all_teachers(sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                           year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
    """Returns the id and names of teachers in MADI"""

    response = requests.post(request_url.format("task8_prepview.php"),
                             data={'step_no': '2',
                                   'task_id': '8',
                                   'tp_year': year,
                                   'sem_no': sem,
                                   'cur_prep': '0'})

    html = bs(response.text, 'lxml')
    teachers = html.find_all('option')

    if len(teachers) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()

    for teacher in teachers:
        if int(teacher['value']) > 0:
            data[teacher['value']] = remove_spaces(teacher.text)

    return data


@router.get('/{id}')
async def get_teacher_name(id: int):

    """Return ID of teacher"""

    all_teachers: dict = await get_all_teachers()

    try:
        data = {str(id): all_teachers[str(id)]}
    except:
        raise HTTPException(404, detail='Not found')

    return data


@router.get('/{id}/exam/')
async def get_teacher_exam(id: int,
                           sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                           year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):

    """Returns JSON exam of teacher by id and year"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '4',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem}',
                                   'pr_id': f'{id}'})

    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)

    name = (await get_teacher_name(id))
    data = Teacher.exam_schedule(html=tables[1], teacher_name=name[str(id)])

    return data.dict(exclude_none=True)


@router.get('/{id}/schedule/')
async def get_teacher_schedule(id: int,
                               sem: Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                               year: Annotated[int, Path(ge=19, le=99)] = get_current_year()):

    """Returns JSON teacher schudule"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '8',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem}',
                                   'pr_id': f'{id}'})

    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)
    
    name = (await get_teacher_name(id))
    data = Teacher.get_schedule(html=tables[1], teacher_name=name[str(id)])

    return data.dict
