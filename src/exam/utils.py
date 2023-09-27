from bs4 import BeautifulSoup as bs
from utils import convert_to_dict_time, remove_garbage
from groups.schemas import (
    Group,
    Exam as GroupExam,
    Lesson as GroupLesson,
    )
from teachers.schemas import (
    Teacher,
    Exam as TeacherExam,
    Lesson as TeacherLesson,
)
import models
from .generators import exam as gen_exam

async def parseGroupExam(html: bs, group: Group | str = None) -> GroupExam:
    data = GroupExam(
        group = group,
        exams = list()
    )
    for exam in gen_exam(html):
        exam_date_time = exam[1].split(' ')
        time = convert_to_dict_time(exam_date_time[1])
        data.exams.append(GroupLesson(
            date=models.Date(
                day=exam_date_time[0],
                time=models.Time(start=time['start'], end=time['end'])
            ),
            type='Экзамен',
            discipline=exam[0],
            auditorium=exam[2],
            teacher=Teacher(value=remove_garbage(exam[3], ['..']))
        ))
    return data


async def parseTeacherExam(html: bs, teacher: Teacher = None) -> TeacherExam:
    data = TeacherExam(
        teacher=teacher,
        exams=list()
    )
    for exam in gen_exam(html):
        exam_date_time = exam[1].split(' ')
        time = convert_to_dict_time(exam_date_time[1])
        data.exams.append(TeacherLesson(
            date = models.Date(
                day = exam_date_time[0],
                time = models.Time(
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