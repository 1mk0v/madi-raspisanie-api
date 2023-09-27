from . import Interface
from typing import List, Dict
from sqlalchemy import Table 
from models import (
    Date as DateModel,
    Time as TimeModel,
    Teacher,
    Group
)
from database.schemas import *
from exam.schemas import Exam as ExamModel
from groups.schemas import GroupLesson
from teachers.schemas import TeacherLesson
from database.schemas import Exam as ExamDBModel
from .base import *

class ExamInfoDB(Interface):

    async def __get_value(self, schema:Table, col_name:str, el_name:str, element, col_num:int = 1):
        res = await self.db.fetch_val(query=schema.select().where(schema.c[col_name] == element[el_name]),
                                      column=col_num)
        return res
    
    async def get_one(self, exam:ExamDBModel):
        query = self.schema.select().where(
            self.schema.c.date_id == exam.date_id,
            self.schema.c.discipline_id == exam.lesson_id,
            self.schema.c.type_id == exam.type_id,
            self.schema.c.auditorium_id == exam.auditorium_id,
            self.schema.c.teacher_id == exam.teacher_id,
            self.schema.c.group_id == exam.group_id,

        )
        return self._is_Empty(await self.db.fetch_one(query))
    
    async def format(self,data:List):
        for element in data:
            date_info = await self.db.fetch_one(query=date.select().where(date.c['id'] == element['date_id']))
            frequency_info = await self.__get_value(frequency, "id", "frequency_id", date_info, 1)
            time_info = await self.db.fetch_one(query=time.select().where(time.c['id'] == date_info['time_id']))
            discipline_info = await self.__get_value(discipline, "id", "discipline_id", element, 1 )
            type_info = await self.__get_value(type, "id", "type_id", element, 1)
            auditorium_info = await self.__get_value(auditorium, "id", "auditorium_id", element, 2)
            teacher_info = await self.db.fetch_one(query=teacher.select().where(teacher.c['id'] == element['teacher_id']))
            group_info = await self.db.fetch_one(query=group.select().where(group.c['id'] == element['group_id']))
            yield ExamModel( 
                date=DateModel(
                    day=date_info['day'],
                    friequency=frequency_info,
                    time = None if time_info == None else TimeModel(
                        start=time_info['start'],
                        end=time_info['end']
                    )
                ),
                discipline = discipline_info,
                type = type_info,
                auditorium = auditorium_info,
                teacher = None if teacher_info == None else teacher_info,
                group = None if group == None else group_info
            )
    
    async def get_by_group(self, id:int) -> List[ExamModel]:
        data = await self.get_by_column('group_id', id)
        exam = list()
        async for element in self.format(data=data):
            exam.append(element)
        return exam


    async def get_by_teacher(self, id:int) -> List[ExamModel]:
        data = await self.get_by_column('teacher_id', id)
        exam = list()
        async for element in self.format(data=data):
            exam.append(
                ExamModel(
                    date=element.date,
                    discipline=element.discipline,
                    type=element.type,
                    auditorium=element.auditorium,
                    group=element.group
                ))
        return exam


    async def add(
        self,
        exam:ExamDBModel
    ):
        try:
            return (await self.get_one(exam))['id']
        except:
            query = self.schema.insert().values(
                date_id=exam.date_id,
                discipline_id=exam.lesson_id,
                type_id=exam.type_id,
                auditorium_id=exam.auditorium_id,
                teacher_id=exam.teacher_id,
                group_id=exam.group_id)
            return self._is_Empty(await self.db.execute(query))
    
    

DBExamInfo = ExamInfoDB(
    model=ExamModel,
    schema=exam
)