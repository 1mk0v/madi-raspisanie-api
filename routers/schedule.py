import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse

import json
from fastapi import APIRouter
from .groups import get_group_schedule
router = APIRouter(prefix='/schedule', tags=['Schedules'])

from routers import request_url


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
    #         schedule = await get_group_schedule(tag['value'])
    #     except Exception as error:
    #         schedule = {'Пока его нет('}
    #     data[tag['value']] = {
    #         'group_name': tag.text,
    #         'value': schedule
    #     }
    #     print(tag['value'], 'is parsed')
    # pass