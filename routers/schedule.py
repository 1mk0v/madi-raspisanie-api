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
    pass
    # data = dict()
    # response = requests.get(request_url.format('task3,7_fastview.php'))
    # html = bs(response.text, 'lxml').find_all('li')
    # for tag in html:
    #     schedule:dict
    #     try:
    #         schedule = get_group_schedule(tag['value'])
    #     except Exception as error:
    #         schedule = {'Пока его нет('}
    #     data[tag['value']] = {
    #         'group_name': tag.text,
    #         'value': schedule
    #     }
    #     print(tag['value'], 'is parsed')
    # return data