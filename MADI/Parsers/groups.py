"""
Модуль `groups`

Тут собраны все методы для парсинга объекта `Group`

"""


from bs4 import BeautifulSoup as bs
from MADI.models import Schedule, Schedule_Info, Exam_Info, Date, Time, Group as Group_Model
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
    def schedule(html: bs, group_name:str = None) -> Schedule_Info:

        """
        Parsing a table with a group exam schedule

        mode показывает режим заполения расписания где
        * 0 - заполнения обычного расписания
        * 1 - заполнения полнодневных занятий
        """

        mode = 0
        schedule:List
        data = Schedule_Info(
            name = Group_Model(
                id = None,
                value = group_name
            ),
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
                    Schedule(
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
                        teacher=remove_garbage(lesson[5])
                    )
                )
            elif mode == 1 and len(lesson) == 3:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
                schedule.append(Schedule(
                        date=Date(
                            friequency=lesson[2]
                        ),
                        discipline=list(),
                        type=lesson[1]
                    )
                )
            elif mode == 1 and len(lesson) == 4:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
                schedule.append(
                    Schedule(
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
    def exam_schedule(html: bs, name:str = None) -> Exam_Info:

        """Parsing a table with a group class schedule"""

        data = Exam_Info(
            name = Group_Model(
                id = None, 
                value = name
            ),
            exam=list()
        )
        for exam in Generators.exam(html):
            exam_date_time = exam[1].split(' ')
            time = convert_to_dict_time(exam_date_time[1])
            data.exam.append(Schedule(
                date=Date(
                    day=exam_date_time[0],
                    time=Time(start=time['start'], end=time['end'])
                ),
                type='Экзамен',
                discipline=exam[0],
                auditorium=exam[2],
                teacher=remove_garbage(exam[3], ['..'])
            ))

        return data