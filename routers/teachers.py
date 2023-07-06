import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse

from fastapi import APIRouter, HTTPException
router = APIRouter(prefix='/teacher', tags=['Teachers'])


request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/all')
def get_all_teachers():

    """Returns JSON info about teachers"""

    response = requests.post(request_url.format("task4_prepexam.php"), 
                             data={'step_no':'1', 'task_id':'4','kaf_presel':''})
    html = bs(response.text, 'lxml')
    teachers = html.find_all('option')
    if len(teachers) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()

    for teacher in teachers:
        if '20' not in teacher.text and 'Выберите преподавателя' not in teacher.text: 
            data[int(teacher['value'])] = teacher.text

    return data


@router.get('/asu_info')
def get_info_of_asu_teachers():
    response = requests.post('https://www.madi.ru/582-kafedra-avtomatizirovannye-sistemy-upravleniya-sotrudnik.html')
    html = bs(response.text, 'lxml')
    teachers = html.find_all('div', class_='row mt-4')
    for teacher in teachers:
        print('https://www.madi.ru/'+teacher.img['src'])
        for i in teacher:
            for j in i:
                if ':' in j.text:
                    for z in j.text.split(':'):
                        if '\xa0' in z:
                            print(z.replace('\xa0', ' ')) 
                else:
                    print(j.text)
        print('\n')
    return {'message':'ok'}
# @router.get('/{id}')