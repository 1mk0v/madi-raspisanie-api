from routers import get_current_sem, get_current_year

import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Department, remove_garbage, remove_spaces, set_selectors

from .teachers import get_teacher_id
from database import schemas, database

from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
router = APIRouter(prefix='/departments', tags=['Departments'])

from routers import request_url

@router.get('/')
async def get_departemnts():
    """Returns departments of MADI"""
    data = dict()
    try:
        response = requests.post(request_url.format("task11_kafview.php"),
                                 data={'task_id': '11',
                                       'step_no': '1',
                                       'kaf_presel': ''})

        html = bs(response.text, 'lxml')
        select = html.find_all('select', {'id':'kf_id'})

        if len(select) == 0:
            raise HTTPException(404, detail=html.text)

        for department in select[0]:
            if int(department['value']) > 0:
                data[department['value']] = remove_spaces(department.text)

    except:

        query = schemas.department.select()
        data = dict(await database.database.fetch_all(query))
        
    return data


@router.get('/{id}/teachers/')
async def get_department_teachers(id:int,
                                  sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                                  year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
    """Returns the id and names of teachers in the department"""
    
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '11',
                                   'kf_id': f'{id}',
                                   'sort': '1',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    
    html = bs(response.text, 'lxml')
    dep_teachers = html.find_all('td', class_='bright')
    
    if len(dep_teachers) == 0:
        raise HTTPException(404, detail=html.text)
    
    teachers = list()
    for teacher in dep_teachers:
        teachers.append(remove_spaces(teacher.text))

    return await get_teacher_id(names=teachers)


@router.get('/{id}/auditoriums')
async def get_department_auditoriums(id:int,
                                     sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                                     year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '11',
                                   'kf_id': f'{id}',
                                   'sort': '2',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    
    html = bs(response.text, 'lxml')
    table = html.find_all('table')
    
    if len(table) < 1:
        raise HTTPException(404, detail=html.text)
    
    auditoriums = list()

    for info in table[1]:
        try:
            auditorium = info.text.split('\n')[3]
            if int(auditorium[:3]) and auditorium not in auditoriums:
                auditoriums.append(auditorium)
        except:
            continue
    
    if len(auditoriums) == 0:
        raise HTTPException(404)

    return {'auditoriums':auditoriums}


@router.get('/{id}/groups')
async def get_department_groups(id:int,
                                sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                                year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()) -> list:
    
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '11',
                                   'kf_id': f'{id}',
                                   'sort': '2',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    
    html = bs(response.text, 'lxml')
    table = html.find_all('table')
    
    schedule = list()
    if len(table) > 0:
        schedule = Department.groups(table[1])
  
    return schedule


@router.get('/{id}/schedule')
async def get_department_groups_schedule(id:int,
                                        sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                                        year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '11',
                                   'kf_id': f'{id}',
                                   'sort': '2',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    
    html = bs(response.text, 'lxml')
    table = html.find_all('table')
    
    if len(table) < 1:
        raise HTTPException(404, detail=html.text)
    
    schedule = Department.groups_schedule(table[1])

    if len(schedule) == 0:
        raise HTTPException(404) 
    
    return {'schedule':schedule}


@router.get('/{id}/exams')
async def get_departemnt_exams(id:int = 61,
                               sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
                               year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year(),
                               selectors:bool= True):
    
    """Returns JSON exams of department"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '10',
                                   'kf_id': f'{id}',
                                   'sort': '1',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) <= 1 :
        p = html.find_all('p')
        raise HTTPException(404, detail=p[0].text)

    data = dict()
    if selectors:
        data['selectors'] = set_selectors(html=tables[0])
    data['schedule'] = Department.exam_schedule(html=tables[1])

    return data