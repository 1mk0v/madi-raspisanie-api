import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Base_methods as madi_parse
from routers import request_url


from fastapi import APIRouter, HTTPException
router = APIRouter(prefix='/group', tags=['Groups'])


async def get_groups_id(name:str=None, names:list=list()): # type: ignore

    groups = await get_groups()
    if len(names) == 0 and name == None:
        raise Exception()

    
    names.append(name)    

    data = dict()
    val_list = list(groups.values())
    key_list = list(groups.keys())

    for name in names:
        try:     
            position = val_list.index(name)
            data[key_list[position]] = name
        except: 
            continue
    return data

@router.get('/')
async def get_groups():
    """Returns all ID's of groups and their names"""

    data = dict()
    response = requests.get(request_url.format('task3,7_fastview.php'))
    html = bs(response.text, 'lxml').find_all('li')
    for tag in html:
        tag_text: str = tag.text
        while '  ' in tag_text:
            tag_text = tag_text.replace('  ', ' ')
        if tag_text[len(tag_text)-1] == ' ':
            tag_text = tag_text.replace(' ', '')
        data[tag['value']] = tag_text
    return data


@router.get('/id')
async def get_group_id(name: str):
    """Returns id of group by their name"""

    data = await get_groups_id(name)
    if len(data) == 0:
        data = {'message': 'Not found'}
   
    return data


@router.get('/{id}/schedule/')
async def get_group_schedule(id:int,
                             selectors:bool=True):

    """Returns JSON schudule of group by id"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        return HTTPException(404, detail=html.text)
    
    data = dict()
    if selectors:
        data['selectors'] = madi_parse.selectors(html=tables[0])
    data['schedule'] = madi_parse.group_schedule(html=tables[1])

    return data


@router.get('/{id}/exam/')
async def get_group_exams(id: int):
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
    data['schedule'] = madi_parse.group_exam_schedule(html=tables[1])

    return data

# @router.post('/add')
# async def add_group(id: int):
#     """Add group by id"""
    
#     pass
