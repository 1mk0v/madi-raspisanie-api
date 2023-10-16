from bs4 import BeautifulSoup as bs
from models import Date, Time
from .schemas import Group, GroupLesson, Schedule, Exam, Teacher
from utils import convert_to_dict_time, remove_garbage
from schedule.generators import exam as gen_exam, lesson as gen_lesson
from typing import List


def schedule(html: bs, group:Group | str = None) -> Schedule:
        #TODO - сократить и привести в читабельный вид (КОД Г...О)
        mode = 0
        schedule:List
        data = Schedule(
            group = group,
            schedule = dict()
        )
        for lesson in gen_lesson(html):
            if "Полнодневные занятия" in lesson:
                mode = 1
            elif mode == 0 and len(lesson) == 1:
                data.schedule[lesson[0]] = list()
                schedule = data.schedule[lesson[0]]
            elif mode == 0 and len(lesson) > 1:
                time=convert_to_dict_time(lesson[0])
                schedule.append(
                    GroupLesson(
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
                schedule.append(GroupLesson(
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
                    GroupLesson(
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


def exam(html: bs, group:Group = None) -> Exam:

        """Parsing a table with a group class schedule"""

        data = Exam(
            group = group,
            exams = list()
        )
        for exam in gen_exam(html):
            exam_date_time = exam[1].split(' ')
            time = convert_to_dict_time(exam_date_time[1])
            data.exams.append(GroupLesson(
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