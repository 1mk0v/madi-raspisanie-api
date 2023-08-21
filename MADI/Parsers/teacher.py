from bs4 import BeautifulSoup as bs
from .schedule import Generators
from MADI.models import Schedule_Info, Schedule, Teacher as Teacher_Model, Group, Date, Time, Exam_Info
from MADI.main import *

class Teacher():
    
    """
        Teacher parsing methods
    """
        
    @staticmethod
    def get_schedule(html: bs, teacher_name:str = None) -> Schedule_Info:

        """Parsing HTML table of schedule"""
        
        data = Schedule_Info(
            name=Teacher_Model(
                id = None,
                value = teacher_name
            ),
            schedule=dict()
        )
    
        schedule:List
        for lesson in Generators.schedule(html):
            if len(lesson) == 1:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
            else:
                time=convert_to_dict_time(lesson[0])
                schedule.append(Schedule(
                    group=Group(
                        id = None,
                        value = remove_spaces(lesson[1])
                    ),
                    discipline = lesson[2],
                    date = Date(
                        friequency = lesson[4],
                        time = Time(
                            start=time['start'],
                            end=time['end']
                        )
                    ),
                    type = lesson[3],
                    auditorium = lesson[5]))
            
        return data
    
    
    @staticmethod
    def exam_schedule(html: bs, teacher_name:str = None) -> Exam_Info:

        """Parsing a table with a group class schedule"""

        data = Exam_Info(
            name=Teacher_Model(
                id = None,
                value=teacher_name
            ),
            exam=list()
        )

        for exam in Generators.exam(html):
            exam_date_time = exam[1].split(' ')
            time = convert_to_dict_time(exam_date_time[1])
            data.exam.append(Schedule(
                date = Date(
                    day = exam_date_time[0],
                    time = Time(
                        start=time['start'],
                        end=time['end']
                    )
                ),
                group = Group(
                    id = None,
                    value = exam[0]
                ),
                discipline=exam[3],
                auditorium=exam[2]
            ))
        return data