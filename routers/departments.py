import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse
from datetime import datetime

from .teachers import get_teacher_id
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
router = APIRouter(prefix='/departments', tags=['Departments'])

request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'



@router.get('/')
async def get_departemnts():
    """Returns departments of MADI"""

    response = requests.post(request_url.format("task11_kafview.php"),
                             data={'task_id': '11',
                                   'step_no': '1',
                                   'kaf_presel': ''})
    
    html = bs(response.text, 'lxml')
    options = html.find_all('option')

    if len(options) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()
    for department in options:
        if int(department['value']) > 0:
            data[department['value']] = madi_parse.remove_spaces(department.text) 

    return data


@router.get('/{id}/teachers/')
async def get_department_teachers(id:int,
                            sem_number:int = 1, #1 - Осенний семестр, 2 - Весений семестр
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
    """tab: 11
    kf_id: 61
    kf_name: Автоматизированных систем управления
    sort: 2
    tp_year: 22
    sem_no: 2"""
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '11',
                                   'kf_id': f'{id}',
                                   'sort': '1',
                                   'tp_year': f'{year}',
                                   'sem_no': f'{sem_number}'})
    pass

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

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.department_exam_schedule(html=tables[1])

    return data


