from bs4 import BeautifulSoup as bs
from .models import *
from .main import *

class Teacher:
    
    def __init__(self) -> None:
        pass


    @staticmethod
    def get_schedule(html: bs, teacher_name:str = None) -> Schedule_Info:

        """Parsing a table with a ASU exam schedule"""
        
        data = Schedule_Info(sorted_by=teacher_name ,schedule={})
        date = 0
        tr:List[bs] = html.find_all('tr')
        for element in tr:
            schedule = delete_empty_elements(element.get_text().split('\n'))
            week = element.find('th')
            if week != None and week.attrs['colspan'] == '6':
                date = remove_garbage(schedule[0])
                data.schedule[date] = list()
            if len(schedule) > 1:
                data.schedule[date].append(Schedule(
                    group=remove_spaces(schedule[1]),
                    discipline=schedule[2],
                    date=Date(
                        friequency=schedule[4],
                        time=schedule[0]
                    ),
                    type=schedule[3],
                    auditorium=schedule[5]))
                
        return data
    
    
    @staticmethod
    def exam_schedule(html: bs, teacher_name:str = None) -> Exam_Info:

        """Parsing a table with a group class schedule"""

        data = Exam_Info(name=teacher_name ,exam=list())
        tr:bs = html.find_all('tr')
        for element in tr:
            exam = delete_empty_elements(element.get_text().split('\n')) 
            if 'Группа' not in exam[0] and len(exam) > 3:
                exam_date_time = exam[1].split(' ')
                data.exam.append(Schedule(
                    date=Date(
                        day=exam_date_time[0],
                        time=exam_date_time[1]
                    ),
                    group=exam[0],
                    discipline=exam[3],
                    auditorium=exam[2]
                ))

        return data