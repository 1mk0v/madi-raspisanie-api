"""
    `Site` - класс с приватными методами для составления запросов на сайт. 
    От него наследуются остальные классы с более точной информацией для запроса, такие как:

    * `Group` - 
    * `Teacher` -
"""

import requests
from bs4 import BeautifulSoup as bs

URL = 'https://raspisanie.madi.ru/tplan/tasks/{}'

class Site():

    """
        Методы для составления запросов с сайта МАДИ
        Актуальный сайт на 2023 год https://raspisanie.madi.ru/tplan
    """

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

    """
        Методы для получения данных с сайта МАДИ относительно группы

        * `get` - вернет все группы на данный учебный год
        * `get_schedule`- вернет расписание определенной группы 
        * `get_exam` - вернет расписание экзаменов определенной группы

    """

    def __init__(self) -> None:
        super().__init__()

    async def get(self) -> bs:
        """
        Use get request of `requests` and `bs4` libs

        Returns:
            bs
        """
        response = self._get(
            url='task3,7_fastview.php'
            )
        return self._is_Empty(
            response=response,
            page_element='li')

    
    async def get_schedule(self, id:int, sem:int, year:int, name:str = None) -> bs:
        """
            Чтобы получить новое расписание, нужно убрать с параметров семестр и год.
            #TODO - исправить данный недочет (от 25.08.23)
        """
        response = self._schedule(
            data={
                'tab':'7',
                'gp_name': f'{name}',
                'gp_id':f'{id}',
                # 'sem_no': f'',
                # 'tp_year': f''
                }
            )
        return self._is_Empty(
            response=response,
            page_element='table',
            detail=response.text
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
    
    """
        Use get request of `requests` and `bs4` libs

        Returns:
            bs
    """
    def __init__(self) -> None:
        super().__init__()

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
            page_element='option'
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