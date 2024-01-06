from requests import Response
from . import BaseRequests
from typing import List
from bs4 import BeautifulSoup as bs
import exceptions as exc


class RaspisanieMADI(BaseRequests):

    """
        Методы для составления запросов с сайта МАДИ
        Актуальный сайт на 2023 год https://raspisanie.madi.ru/tplan
    """

    def __init__(self, url: str = 'https://raspisanie.madi.ru/tplan/tasks/{}') -> None:
        super().__init__(url)

        
    def find_and_return_exceptions(func):
        def wrapper(*args, **kwargs):
            status_code = kwargs['response'].status_code
            if status_code > 399 and status_code < 500:
                raise exc.NotFoundError(
                    status_code=status_code,
                    detail=bs(kwargs['response'].text, 'lxml').find(name='p').text
                )
            return func(*args, **kwargs)
        return wrapper

    @find_and_return_exceptions
    def _getPageElementOrException(self, response: Response, page_element: str, class_name: str = None, detail: str = None) -> List[bs] | bs:
        return super()._getPageElementOrException(response, page_element, class_name, detail)
    

class RaspisanieGroups(RaspisanieMADI):

    def __init__(self) -> None:
        super().__init__()

    async def get(self) -> bs:

        response = self._get(
            url='task3,7_fastview.php'
            )
        return self._getPageElementOrException(
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
        return self._getPageElementOrException(
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
        return self._getPageElementOrException(
            response=response,
            page_element='table',
            class_name='timetable',
            detail=f'The are no exams for group ID {id}'
        )[0]
    

class RaspisanieTeachers(RaspisanieMADI):
    
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
        return self._getPageElementOrException(
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
        return self._getPageElementOrException(
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
        return self._getPageElementOrException(
            response=response,
            page_element='table',
            class_name='timetable',
            detail=f'The are no schedule for teacher ID {id}'
        )[0]
    

class RaspisanieDepartments(RaspisanieMADI):

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
        return self._getPageElementOrException(
            response=response,
            page_element='option',
            detail='Schedule of department not found'
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
        return self._getPageElementOrException(
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
        return self._getPageElementOrException(
            response=response,
            page_element='table',
            class_name='timetable',
            detail='Department auditoriums not found'
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
        return self._getPageElementOrException(
            response=response,
            page_element='table',
            class_name='timetable',
            detail='Department schedule not found'
        )[0]