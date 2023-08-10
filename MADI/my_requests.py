import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

URL = 'https://raspisanie.madi.ru/tplan/tasks/{}'

def get_current_year() -> int():

    """Return current year"""

    current_academic_year:int = int(datetime.today().strftime("%Y"))-2001 
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_academic_year -= 1

    return current_academic_year


def get_current_sem() -> int():

    """Return current semester"""
    
    current_sem = 2
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_sem = 1

    return current_sem


class Site():

    def __init__(self) -> None:
        pass

    def _get(self, url, data = None) -> requests.Response:
        return requests.get(URL.format(url), data)
    
    def _post(self, url, data = None) -> requests.Response:
        return requests.post(URL.format(url), data)
    
    def _schedule(self, data) -> requests.Response:
        return self._post(url="tableFiller.php", data=data)

    def _is_Empty(self, response:requests.Response, page_element:str, detail:str='Not found') -> bs:
        html = bs(response.text, 'lxml').find_all(page_element)
        if len(html) < 1:
            raise ValueError(detail)
        if page_element == 'table':
            html = html[1]
        return html

class Groups(Site):

    def __init__(self) -> None:
        super().__init__()

    async def get(self) -> bs:
        response = self._get(
            url='task3,7_fastview.php'
            )
        return self._is_Empty(
            response=response,
            page_element='li')

    async def get_schedule(self, id:int, sem:int, year:int, name:str = None) -> bs:
        response = self._schedule(
            data={
                'tab':'7',
                'gp_name': f'{name}',
                'gp_id':f'{id}',
                'sem_no': f'{sem}',
                'tp_year': f'{year}'
                }
            )
        return self._is_Empty(
            response=response,
            page_element='table',
            detail=f'The are no schedule for group ID {id}'
            )

    async def get_exam(self, id:int, sem:int, year:int, name:str= None) -> bs:
        response = self._schedule(
            data={
                'tab': '3',
                'gp_name': f'{name}',
                'gp_id':f'{id}',
                'sem_no': f'{sem}',
                'tp_year': f'{year}'
                }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            detail=f'The are no exams for group ID {id}'
        )


class Teachers(Site):
    
    def __init__(self) -> None:
        pass

    async def get(self, year:int, sem:int) -> bs: 
        response = self._post(
            url = "task8_prepview.php",
            data={
                'step_no': 2,
                'task_id': 8,
                'tp_year': year,
                'sem_no': sem,
                'cur_prep': 0
                }
            )
        return self._is_Empty(
            response=response,
            page_element='option',
        )

    async def get_schedule(self, id:int, year:int, sem:int) -> bs:
        response = self._schedule(
            data={
                'tab': '8',
                'tp_year': f'{year}',
                'sem_no': f'{sem}',
                'pr_id': f'{id}'
            }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            detail=f'The are no schedule for teacher ID {id}')
    
    async def get_exam(self, id:int, year:int, sem:int) -> bs:
        response = self._schedule(
            data={
                'tab': '4',
                'tp_year': f'{year}',
                'sem_no': f'{sem}',
                'pr_id': f'{id}'
            }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            detail=f'The are no schedule for teacher ID {id}')