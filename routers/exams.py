import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse

from fastapi import APIRouter, HTTPException
router = APIRouter(prefix='/exam', tags=['Exams'])

request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/asu')
async def get_all_asu_exams(year: int = 22,selectors:bool= True):
    """Returns JSON exams of ASU"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '10',
                                   'kf_id': '61',
                                   'kf_name': 'Автоматизированных систем управления',
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
    data['schedule'] = madi_parse.asu_exam_schedule(html=tables[1])

    return data


@router.get('/{id}')
async def get_exam_by_id_group(id: int):
    """Returns JSON exams of group by id"""

    response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '3',
                                   'gp_id': f'{id}'})
    
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)

    data = dict()
    data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.exam_schedule(html=tables[1])

    return data
