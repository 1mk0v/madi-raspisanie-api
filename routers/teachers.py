import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse
from datetime import datetime 
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
router = APIRouter(prefix='/teacher', tags=['Teachers'])

request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/')
def get_all_teachers():
    """Returns JSON info about teachers"""

    response = requests.post(request_url.format("task4_prepexam.php"), 
                             data={'step_no':'1',
                                   'task_id':'4',
                                   'kaf_presel':''})
    
    html = bs(response.text, 'lxml')
    teachers = html.find_all('option')

    if len(teachers) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()

    for teacher in teachers:
        if '20' not in teacher.text and 'Выберите преподавателя' not in teacher.text: 
            data[int(teacher['value'])] = madi_parse.remove_spaces(teacher.text) 

    return data


@router.get('/asu')
def get_asu_teachers():
    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '10',
                                   'kf_id': '61',
                                   'kf_name': 'Автоматизированных систем управления',
                                   'sort': '2',
                                   'tp_year': f'{int(datetime.today().strftime("%Y"))-2001}',
                                   'sem_no': '2'})
    html = bs(response.text, 'lxml')
    asu_teachers = html.find_all('th')
    

    if len(asu_teachers) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    all_teachers:dict = get_all_teachers()
    val_list = list(all_teachers.values())

    for tag in asu_teachers:
        try:
            if tag['colspan']:
                name = madi_parse.remove_spaces(tag.text)
                if name in val_list:
                    key_list = list(all_teachers.keys())
                    position = val_list.index(name)
                    data[key_list[position]] = name
        except:
            continue
    
    return data


@router.get('/id')
async def get_id_of_teacher_name(name:str): 
    
    """Return ID of teacher"""

    data = {
        'name': name,
        'result':'Not found'
    }

    all_teachers:dict = get_all_teachers()
    val_list = list(all_teachers.values())

    if name in val_list:
        key_list = list(all_teachers.keys())
        position = val_list.index(name)
        data = {
            'name': name,
            'result':key_list[position]
            }

    return data


@router.get('/exams/{id}')
async def get_exam_by_teacher_id(id: int,
                           year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001,
                           selectors: bool = True):
    
    """Returns JSON exams of teacher by id and year"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '4',
                                   'tp_year': f'{year}',
                                   'sem_no': '2',
                                   'pr_id': f'{id}'})

    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()
    data['teacher'] = get_all_teachers()[id]
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.exam_schedule(html=tables[1])

    return data