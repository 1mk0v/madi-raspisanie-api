import requests
from bs4 import BeautifulSoup as bs
from Madi_parsing_module.main import Group, remove_garbage, remove_spaces, set_selectors
from Madi_parsing_module.models import *
from routers import request_url

from fastapi import APIRouter, HTTPException
router = APIRouter(prefix='/group', tags=['Groups'])


async def get_groups_id(name:str=None, names:list=list()): 

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
async def get_groups() -> Dict[str,str]:
    """Returns all ID's of groups and their names"""

    data = dict()
    response = requests.get(request_url.format('task3,7_fastview.php'))
    html = bs(response.text, 'lxml').find_all('li')
    for tag in html:
        data[tag['value']] = remove_spaces(tag.text)
    return data


@router.get('/{id}')
async def get_group_name(id: str) -> Dict[str, str]:

    """Returns id of group by their name"""
    groups: dict = await get_groups()

    try:
        data = {str(id): groups[str(id)]}
    except:
        raise HTTPException(404, detail='Not found')

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

    data = Group.exam_schedule(html=tables[1])

    return data.dict(exclude_none=True)


@router.get('/{id}/schedule/')
async def get_group_schedule(id:int):

    """Returns JSON schudule of group by id"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        return HTTPException(404, detail=html.text)
    
    group_name = (await get_group_name(str(id)))

    data = Group.schedule(html=tables[1], group_name=group_name[str(id)])

    return data.dict(exclude_none=True)


# @router.post('/add')
# async def add_group(id: int):
#     """Add group by id"""
    
#     pass
