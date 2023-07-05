import requests
from bs4 import BeautifulSoup as bs


from fastapi import APIRouter
router = APIRouter(prefix='/groups', tags=['Group methods'])


request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'


@router.get('/getIds')
def get_ids():

    """Returns all ID's of groups and their names"""

    data = dict()
    response = requests.get(request_url.format('task3,7_fastview.php'))
    html = bs(response.text, 'lxml').find_all('li')
    for tag in html:
        tag_text:str = tag.text
        while '  ' in tag_text:
            tag_text = tag_text.replace('  ', ' ')
        if tag_text[len(tag_text)-1] == ' ':
            tag_text = tag_text.replace(' ', '')
        data[tag['value']] = tag_text
    return data


@router.get('/getIdByName')
def get_id_by_name(name:str):

    """Returns id of group by their name"""

    data = {'message': 'Not found'}
    groups:dict = get_ids()
    val_list = list(groups.values())
    if name in val_list:
        key_list = list(groups.keys())
        position = val_list.index(name)
        data['message'] = key_list[position]
    return data 