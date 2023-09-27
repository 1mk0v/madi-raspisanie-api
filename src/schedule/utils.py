from bs4 import BeautifulSoup as bs
from typing import List
from utils import convert_to_dict_time, remove_garbage, get_current_sem, get_current_year, findValueInListHTML
from groups.schemas import (
    Group,
    Schedule as GroupSchedule,
    Lesson as GroupLesson,
    )
from teachers.schemas import (
    Teacher,
    Schedule as TeacherSchedule,
    Lesson as TeacherLesson,
)
from department.schemas import (
    Department,
    DepartmentSchedule, 
    Schedule as DepartmentLesson
)
import madi
import models
from .generators import lesson as gen_lesson
weekdaysList = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

async def parseGroupSchedule(html: bs, group: Group | str = None) -> GroupSchedule:
    mode = 0
    schedule: List
    data = GroupSchedule(group=group, schedule=dict())
    for lesson in gen_lesson(html):
        if "Полнодневные занятия" in lesson:
            mode = 1
        elif mode == 0 and len(lesson) == 1:
            data.schedule[lesson[0]] = list()
            schedule = data.schedule[lesson[0]]
        elif mode == 0 and len(lesson) > 1:
            time = convert_to_dict_time(lesson[0])
            schedule.append(
                GroupLesson(
                    date=models.Date(
                        time=models.Time(start=time["start"], end=time["end"]),
                        friequency=lesson[3],
                    ),
                    discipline=lesson[1],
                    type=remove_garbage(lesson[2]),
                    auditorium=lesson[4],
                    teacher=Teacher(value=remove_garbage(lesson[5])),
                )
            )
        elif mode == 1 and (len(lesson) == 3 or len(lesson) == 4):
            try:
                data.schedule[lesson[0]]
            except:
                data.schedule[lesson[0]] = list()
            schedule = data.schedule[lesson[0]]
            schedule.append(
                GroupLesson(
                    date=models.Date(friequency=lesson[-1]),
                    discipline=list(),
                    type=lesson[-2],
                )
            )
            if len(lesson) == 4:
                schedule[-1].discipline.append(lesson[-3])

    return data


async def parseTeacherSchedule(html: bs, teacher: Teacher = None) -> TeacherSchedule:
    data = TeacherSchedule(
        teacher=teacher,
        schedule=dict()
    )
    schedule: List
    for lesson in gen_lesson(html):
        if len(lesson) == 1:
            data.schedule[lesson[0]] = list()
            schedule = data.schedule[lesson[0]]
        else:
            time = convert_to_dict_time(lesson[0])
            schedule.append(
                TeacherLesson(
                    group=Group(
                        id=None,
                        value=remove_garbage(lesson[1])
                    ),
                    discipline=lesson[2],
                    date=models.Date(
                        friequency=lesson[4],
                        time=models.Time(
                            start=time['start'],
                            end=time['end']
                        )
                    ),
                    type=lesson[3],
                    auditorium=lesson[5]
                )
            )

    return data


async def parseDepartmentSchedule(html: bs, department:Department = None,) -> DepartmentSchedule:
    raspisanieTeacher = madi.RaspisanieTeachers()
    raspisanieGroup = madi.RaspisanieGroups()
    groupHTML = await raspisanieGroup.get()
    teacherHTML = await raspisanieTeacher.get(year=get_current_year(), sem=get_current_sem())
    allTeachersList = [element.text for element in teacherHTML]
    allGroupsList = [element.text for element in groupHTML]
    data = DepartmentSchedule(department=department, schedule=dict())
    teacher:Teacher
    weekday = ''
    storageAddWeeks = []
    for lesson in gen_lesson(html):
        if len(lesson) == 1 and lesson[0] not in weekdaysList:
            teacher = await findValueInListHTML(value=lesson[0], list=allTeachersList, 
                                                html=teacherHTML, model=Teacher)
            teacher.department_id = department.id
        elif len(lesson) > 2:
            time = convert_to_dict_time(lesson[0])
            group:Group = await findValueInListHTML(value=lesson[3], list=allGroupsList, 
                                                html=groupHTML, model=Group)
            data.schedule[weekday].append(DepartmentLesson
                (
                    group=group,
                    teacher = teacher,
                    discipline=lesson[4],
                    date=models.Date(
                        friequency=lesson[1],
                        time=models.Time(
                            start=time['start'],
                            end=time['end']
                        )
                    ),
                    type=lesson[5],
                    auditorium=lesson[2]
                )
            )
        else:
            weekday = lesson[0]
            if weekday not in storageAddWeeks:
                storageAddWeeks.append(weekday)
                data.schedule[weekday] = list()
    return data    