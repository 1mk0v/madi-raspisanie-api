from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup as bs
import requests

app = FastAPI(title='MADI ASU Terminal API')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'

@app.get('/getGroupsId')
def get_groups_id():
    data = dict()
    response = requests.get(request_url.format('task3,7_fastview.php'))
    founded_tags = bs(response.text, 'lxml').find_all('li')
    for tag in founded_tags:
        tag_text:str = tag.text
        while '  ' in tag_text:
            tag_text = tag_text.replace('  ', ' ')
        if tag_text[len(tag_text)-1] == ' ':
            tag_text = tag_text.replace(' ', '')
        data[tag['value']] = tag_text
    return data


@app.get('/getGroupIdByName')
def get_group_id_by_name(name:str):
    data = {'message': 'Not found'}
    groups:dict = get_groups_id()
    val_list = list(groups.values())
    if name in val_list:
        key_list = list(groups.keys())
        position = val_list.index(name)
        data['message'] = key_list[position]
    return data 
    

@app.get('/getTimetable')
def get_group_timetable_by_id(id:int):
    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    founded_tags = bs(response.text, 'lxml')
    tables = founded_tags.find_all('table')
    if len(tables) == 0:
        raise HTTPException(404, detail=founded_tags.text)
    headers_info = list()

    for tag in tables[0]:
        try:
            headers_info.append({'name': tag.th.text, 'value': tag.td.text})
        except:
            continue

    # for tag in tables[1]:
    #     for tr in tag:
    #         try:
    #             headers_info.append({'name': tr.td.text, 'value': tag.td.text})
    #         except:
    #             continue

    return {'message': 'ok'}
