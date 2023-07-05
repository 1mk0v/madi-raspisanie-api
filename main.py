from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup as bs
import requests
from Madi_parsing_module.main import Base_methods as madi_parse 


from routers import groups

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

app.include_router(groups.router)

@app.get('/getTimetable')
def get_group_timetable_by_id(id:int):

    """Returns JSON schudule of group by id"""

    response = requests.post(request_url.format("tableFiller.php"), 
                             data={'tab':'7', 'gp_id':f'{id}'})
    html = bs(response.text, 'lxml')
    tables = html.find_all('table')

    if len(tables) == 0:
        raise HTTPException(404, detail=html.text)
    
    data = dict()
    data['selectors'] = madi_parse.selectors(html=tables[0])
    data['timetable'] = madi_parse.timetable(html=tables[1])

    return data

