"""
Модуль `groups`

Тут собраны все методы для парсинга объекта `Group`

"""

from bs4 import BeautifulSoup as bs
from MADI.models import (
    Schedule_Group_Info,
    Exam_Group_Info,
    Schedule_Group,
    Teacher,
    Date,
    Time,
    Group as Group_Model
)
from .schedule import Generators
from typing import List
from MADI.main import remove_garbage, convert_to_dict_time

class Group:

    """
        Методы парсинга для расписаний группы
        
        * Вы можете парсить HTML страницу `расписания занятий` группы
        * Вы можете парсить HTML страницу `расписания экзаменов` группы
        
        
    """

    def __init__(self) -> None:
        pass


    @staticmethod
    def schedule(html: bs, group:Group_Model | str = None) -> Schedule_Group_Info:

        """
        Parsing a table with a group exam schedule

        mode показывает режим заполения расписания где
        * 0 - заполнения обычного расписания
        * 1 - заполнения полнодневных занятий
        
        9313 8744 8745 8746 8748 - problems ID's
        """

        mode = 0
        schedule:List
        data = Schedule_Group_Info(
            group_info = group,
            schedule = dict()
        )
        for lesson in Generators.schedule(html):
            if "Полнодневные занятия" in lesson:
                mode = 1
            elif mode == 0 and len(lesson) == 1:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
            elif mode == 0 and len(lesson) > 1:
                time=convert_to_dict_time(lesson[0])
                schedule.append(
                    Schedule_Group(
                        date = Date(
                            time = Time(
                                start=time['start'],
                                end=time['end']
                            ),
                            friequency=lesson[3]
                        ),
                        discipline=lesson[1],
                        type=remove_garbage(lesson[2]),
                        auditorium=lesson[4],
                        teacher=Teacher(value=remove_garbage(lesson[5]))
                    )
                )
            elif mode == 1 and len(lesson) == 3:
                try:
                    data.schedule[lesson[0]]
                except:
                    data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
                schedule.append(Schedule_Group(
                        date=Date(
                            friequency=lesson[2]
                        ),
                        discipline=list(),
                        type=lesson[1]
                    )
                )
            elif mode == 1 and len(lesson) == 4:
                try:
                    data.schedule[lesson[0]]
                except:
                    data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
                schedule.append(
                    Schedule_Group(
                        date=Date(
                            friequency=lesson[3]
                        ),
                        discipline=[lesson[1]],
                        type=lesson[2]
                    )
                )
            elif mode == 1 and len(lesson) == 1:
                last_list_el = len(schedule)-1
                schedule[last_list_el].discipline.append(lesson[0])

        return data
    
    @staticmethod
    def exam_schedule(html: bs, group:Group_Model = None) -> Exam_Group_Info:

        """Parsing a table with a group class schedule"""

        data = Exam_Group_Info(
            group_info = group,
            exam = list()
        )
        for exam in Generators.exam(html):
            exam_date_time = exam[1].split(' ')
            time = convert_to_dict_time(exam_date_time[1])
            data.exam.append(Schedule_Group(
                date=Date(
                    day=exam_date_time[0],
                    time=Time(start=time['start'], end=time['end'])
                ),
                type='Экзамен',
                discipline=exam[0],
                auditorium=exam[2],
                teacher=Teacher(value=remove_garbage(exam[3], ['..']))
            ))

        return data