"""
    Модуль для составления запросов к сайту МАДИ с расписанием

    * `Group` - 
    * `Teacher` -
"""

import requests
from typing import List
from bs4 import BeautifulSoup as bs

URL = 'https://raspisanie.madi.ru/tplan/tasks/{}'

class RaspisanieMADI():

    """
        Методы для составления запросов с сайта МАДИ
        Актуальный сайт на 2023 год https://raspisanie.madi.ru/tplan
    """

    def __init__(self) -> None:
        pass

    def _get(self, url, data:dict = None) -> requests.Response:
        return requests.get(URL.format(url), data)
    
    def _post(self, url, data:dict = None, ) -> requests.Response:
        return requests.post(URL.format(url), data = data)
    
    def _schedule(self, data:dict) -> requests.Response:
        return self._post(url="tableFiller.php", data=data)

    def _is_Empty(self, response:requests.Response, page_element:str, class_name:str=None, detail:str='Not found') -> List[bs] | bs:
        html = bs(response.text, 'lxml').find_all(name=page_element, attrs={"class":class_name})
        if len(html) < 1:
            raise ValueError(detail)
        return html

class RaspisanieGroups(RaspisanieMADI):

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
            class_name='timetable',
            detail=response.text
        )[0]

    async def get_exam(self, id:int, sem:int, year:int, name:str= None) -> bs:
        response = self._schedule(
            data={
                'tab': '3',
                'gp_name': f'{name}',
                'gp_id': f'{id}',
                'sem_no': f'{sem}',
                'tp_year': f'{year}'
                }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            class_name='timetable',
            detail=f'The are no exams for group ID {id}'
        )[0]


class RaspisanieTeachers(RaspisanieMADI):
    
    """
        Use get request of `requests` and `bs4` libs

        Returns:
            bs
    """
    def __init__(self) -> None:
        super().__init__()

    async def get(self, year:int, sem:int) -> List[bs] | bs: 
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
            class_name='timetable',
            detail=f'The are no schedule for teacher ID {id}'
        )[0]
    
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
            class_name='timetable',
            detail=f'The are no schedule for teacher ID {id}'
        )[0]


class RaspisanieDepartments(RaspisanieMADI):
    
    """
        Use get request of `requests` and `bs4` libs

        Returns:
            bs
    """

    def __init__(self) -> None:
        super().__init__()

    async def get(self) -> bs: 
        response = self._post(
            url = "task11_kafview.php",
            data={
                'step_no': '1',
                'task_id': '11',
                'kaf_presel':''
                }
            )
        return self._is_Empty(
            response=response,
            page_element='option'
        )
    
    async def get_teachers(self, id:int, sem:int, year:int):
        response = self._schedule(
            data = {
                'tab':'11',
                'kf_id': f'{id}',
                'sort': '1',
                'tp_year': f'{year}',
                'sem_no': f'{sem}'
            }
        )
        return self._is_Empty(
            response=response,
            page_element='td',
            class_name='bright'
        )

    async def get_auditoriums(self, id:int, sem:int, year:int):
        response = self._schedule(
            data = {
                'tab':'11',
                'kf_id': f'{id}',
                'sort': '2',
                'tp_year': f'{year}',
                'sem_no': f'{sem}'
            }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            class_name='timetable',
            detail='Department audits not found'
        )[0]
    
    async def get_schedule(self, id:int, sem:int, year:int):
        response = self._schedule(
            data = {
                'tab':'11',
                'kf_id': f'{id}',
                'sort': '1',
                'tp_year': f'{year}',
                'sem_no': f'{sem}'
            }
        )
        return self._is_Empty(
            response=response,
            page_element='table',
            class_name='timetable',
            detail='Department schedule not found'
        )[0]