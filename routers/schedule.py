import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse
from datetime import datetime

from typing import Annotated
from fastapi import APIRouter, HTTPException , Path
router = APIRouter(prefix='/schedule', tags=['Schedules'])


request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/')
async def get_schedule():

    """Returns JSON schudule of all MADI"""

    data = dict()
    response = requests.get(request_url.format('task3,7_fastview.php'))
    html = bs(response.text, 'lxml').find_all('li')
    for tag in html:
        schedule:dict
        try:
            schedule = get_schedule_by_id_group(tag['value'])
        except Exception as error:
            schedule = {'Пока его нет('}
        data[tag['value']] = {
            'group_name': tag.text,
            'value': schedule
        }
        print(tag['value'], 'is parsed')
    return data



@router.get('/gruop/{id}')
async def get_schedule_by_id_group(id:int, selectors:bool=True):

    """Returns JSON schudule of group by id"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.timetable(html=tables[1])

    return data


@router.get('/teacher/{id}')
async def get_schedule_by_id_teacher(id:int,
                                     year: Annotated[int, Path(ge=19, le=99)] = int(datetime.today().strftime("%Y"))-2001,
                                     selectors:bool=True):

    """Returns JSON teacher schudule"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={
                                   'tab':'8',
                                   'tp_year':f'{year}',
                                   'sem_no':'2',
                                   'pr_id':f'{id}',
                                  })
    
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    print(tables)
    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.teacher_schedule(html=tables[1])

    return data