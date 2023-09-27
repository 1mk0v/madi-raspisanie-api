from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from typing import List
from models import Essence


def getListOfEssences(html:bs, model:Essence = Essence) -> List[Essence]:
    data = list()
    for element in html:
        if int(element['value']) > -1 and '20' not in element.text:
            data.append(model(id=element['value'], value=remove_garbage(element.text)))
    return data

def get_current_year() -> int:
    current_academic_year:int = int(datetime.today().strftime("%Y"))-2000 
    current_month = int(datetime.today().strftime("%m"))
    if current_month < 9:
        current_academic_year -= 1
    return current_academic_year


def get_current_sem() -> int:
    current_sem = 2
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_sem = 1
    return current_sem


def convert_to_dict_time(lesson_time:str) -> dict:
    lesson_time = lesson_time.split(' - ')
    result  = {
        "start":datetime.time(datetime.strptime(lesson_time[0],'%H:%M')) ,
        "end": datetime.time(datetime.strptime(lesson_time[0],'%H:%M') + timedelta(hours=3))
    }
    if len(lesson_time) >= 2:
        result["end"] = datetime.time(datetime.strptime(lesson_time[1],'%H:%M'))
    return result


def remove_spaces(string: str) -> str():

    """Return your input string without double spaces"""

    data = string
    while '  ' in data:
        data = data.replace('  ', ' ')
    if len(data) > 0 and data[len(data)-1] == ' ':
        data = data[:-1]
    return data


def remove_garbage(string: str, symbols: list = []) -> str():

    """Remove garbage from your string"""
    
    name = string
    garbage = ['\n'] + symbols
    for simbol in garbage:
        if simbol in name:
            name = name.replace(simbol, '')
    name = remove_spaces(name)
    return name

def delete_empty_elements(array: List[str]) -> List[str]:
    if array[0] == '' and array[len(array)-1] == '':
        array.pop(0)
        array.pop(len(array) - 1)
    return array

async def findValueInListHTML(value:str | int, list:List, html:bs, model:Essence) -> Essence:
    return model(id = html[list.index(value)]['value'],
                  value = remove_garbage(value))