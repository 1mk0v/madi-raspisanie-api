import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse
from datetime import datetime

from .teachers import get_teacher_id
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
router = APIRouter(prefix='/departments', tags=['Departments'])

from routers import request_url

@router.get('/')
async def get_departemnts():
    """Returns departments of MADI"""

    response = requests.post(request_url.format("task11_kafview.php"),
                             data={'task_id': '11',
                                   'step_no': '1',
                                   'kaf_presel': ''})
    
    html = bs(response.text, 'lxml')
    select = html.find_all('select', {'id':'kf_id'})

    if len(select) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()
    for department in select[0]:
        if int(department['value']) > 0:
            data[department['value']] = madi_parse.remove_spaces(department.text) 

    return data


@router.get('/{id}/teachers/')
async def get_department_teachers(id:int,
                            sem_number:int = 1,
                            year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001):
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
        teachers.append(madi_parse.remove_spaces(teacher.text))

    return get_teacher_id(names=teachers)


@router.get('/{id}/auditoriums')
async def get_department_auditoriums(id:int,
                                     year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001,
                                     sem_number:Annotated[int, Path(ge=1, le=2)] = 2):
    
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
    
    return {'auditoriums':auditoriums}


@router.get('/{id}/schedule')
async def get_department_groups_schedule(id:int,
                                     year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001,
                                     sem_number:Annotated[int, Path(ge=1, le=2)] = 2):
    
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
    
    schedule = madi_parse.department_groups_schedule(table[1])
    
    return {'schedule':schedule}


@router.get('/{id}/exams')
async def get_departemnt_exams(id:int = 61,
                               year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001,
                               selectors:bool= True):
    """Returns JSON exams of ASU"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '10',
                                   'kf_id': f'{id}',
                                   'sort': '1',
                                   'tp_year': f'{year}',
                                   'sem_no': '2'})
    
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) <= 1 :
        p = html.find_all('p')
        raise HTTPException(404, detail=p[0].text)

    data = dict()
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.department_exam_schedule(html=tables[1])

    return data


