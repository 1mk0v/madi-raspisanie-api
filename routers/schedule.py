import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse

from fastapi import APIRouter, HTTPException
router = APIRouter(prefix='/schedule', tags=['Schedules'])


request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/{id}')
def get_schedule_by_id_group(id:int):

    """Returns JSON schudule of group by id"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.timetable(html=tables[1])

    return data

# @router.get('/e{id}')