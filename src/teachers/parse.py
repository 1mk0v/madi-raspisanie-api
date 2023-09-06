from bs4 import BeautifulSoup as bs
from schedule.generators import exam as gen_exam, lesson as gen_lesson
from .schemas import Teacher as TeacherModel, Schedule, Exam, Lesson, Group
from models import Date, Time
from utils import convert_to_dict_time, remove_spaces
from typing import List

def parse_schedule(html: bs, teacher:TeacherModel = None) -> Schedule:

        """Parsing HTML table of schedule"""
        
        data = Schedule(
            teacher=teacher,
            schedule=dict()
        )
    
        schedule:List
        for lesson in gen_lesson(html):
            if len(lesson) == 1:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
            else:
                time=convert_to_dict_time(lesson[0])
                schedule.append(Lesson(
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
    
    

def parse_exam(html: bs, teacher:TeacherModel) -> Exam:

        """Parsing a table with a group class schedule"""

        data = Exam(
            teacher=teacher,
            exams=list()
        )

        for exam in gen_exam(html):
            exam_date_time = exam[1].split(' ')
            time = convert_to_dict_time(exam_date_time[1])
            data.exams.append(Lesson(
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