from . import Interface
from typing import List, Dict
from sqlalchemy import Table 
from models import (
    Date as DateModel,
    Time as TimeModel,
    Teacher,
    Group
)
from schedule.schemas import Schedule as GlobalSchedule
from groups.schemas import GroupLesson
from teachers.schemas import TeacherLesson
from database.schemas import *
from database.models import Schedule
from .base import *
from .group import DBGroups
from .teachers import DBTeacher
from other.db_methods import add, add_date, add_discipline

class ScheduleInfoDB(Interface):

    async def __get_value(self, schema:Table, col_name:str, el_name:str, element, col_num:int = 1):
        res = await self.db.fetch_val(query=schema.select().where(schema.c[col_name] == element[el_name]),
                                      column=col_num)
        return res
    
    async def get_one(self, schedule:Schedule):
        query = self.schema.select().where(
            self.schema.c.weekday_id == schedule.weekday_id,
            self.schema.c.date_id == schedule.date_id,
            self.schema.c.discipline_id == schedule.lesson_id,
            self.schema.c.type_id == schedule.type_id,
            self.schema.c.auditorium_id == schedule.auditorium_id,
            self.schema.c.teacher_id == schedule.teacher_id,
            self.schema.c.group_id == schedule.group_id
        )
        return self._is_Empty(await self.db.fetch_one(query))
    
    async def format(self,data:List):
        for element in data:
            weekday_info = await self.__get_value(weekday, "id", "weekday_id", element,1)
            date_info = await self.db.fetch_one(query=date.select().where(date.c['id'] == element['date_id']))
            frequency_info = await self.__get_value(frequency, "id", "frequency_id", date_info, 1)
            time_info = await self.db.fetch_one(query=time.select().where(time.c['id'] == date_info['time_id']))
            discipline_info = await self.__get_value(discipline, "id", "discipline_id", element, 1 )
            type_info = await self.__get_value(type, "id", "type_id", element, 1)
            auditorium_info = await self.__get_value(auditorium, "id", "auditorium_id", element, 2)
            teacher_info = await self.db.fetch_one(query=teacher.select().where(teacher.c['id'] == element['teacher_id']))
            group_info = await self.db.fetch_one(query=group.select().where(group.c['id'] == element['group_id']))
            yield GlobalSchedule(
                weekday = weekday_info, 
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
                teacher = None if teacher_info == None else Teacher(
                    id = teacher_info['id'] ,
                    value = teacher_info['value'],
                    department_id = teacher_info['department_id']
                ),
                group = None if group == None else Group(
                    id=group_info['id'],
                    value=group_info['value'],
                    department_id=group_info['department_id']
                )
            )
    
    async def get_by_group(self, id:int) -> Dict[str, List[GroupLesson]]:
        data = await self.get_by_column('group_id', id)
        schedule:Dict[str, List[GroupLesson]] = dict()
        weekday:str = ''
        async for element in self.format(data=data):
            if weekday != element.weekday:
                weekday = element.weekday
                schedule[weekday] = list()
            schedule[weekday].append(
                GroupLesson(
                    date=element.date,
                    discipline=element.discipline,
                    type=element.type,
                    auditorium=element.auditorium,
                    teacher=element.teacher
                ))
        return schedule


    async def get_by_teacher(self, id:int):
        data = await self.get_by_column('teacher_id', id)
        schedule:Dict[str, List[TeacherLesson]] = dict()
        weekday:str = ''
        async for element in self.format(data=data):
            if weekday != element.weekday:
                weekday = element.weekday
                schedule[weekday] = list()
            schedule[weekday].append(
                TeacherLesson(
                    date=element.date,
                    discipline=element.discipline,
                    type=element.type,
                    auditorium=element.auditorium,
                    group=element.group
                ))
        return schedule


    async def add(
        self,
        schedule:Schedule
    ):
        try:
            return (await self.get_one(schedule))['id']
        except:
            query = self.schema.insert().values(
                weekday_id=schedule.weekday_id,
                date_id=schedule.date_id,
                discipline_id=schedule.lesson_id,
                type_id=schedule.type_id,
                auditorium_id=schedule.auditorium_id,
                teacher_id=schedule.teacher_id,
                group_id=schedule.group_id)
            return self._is_Empty(await self.db.execute(query))
    
    

DBScheduleInfo = ScheduleInfoDB(
    model=Schedule,
    schema=schedule
)

async def addToAllTableFromSchedule(schedule:GlobalSchedule) -> Schedule:
    return Schedule(
        weekday_id = (await add(DBWeekday, schedule.weekday)).id,
        date_id = (await add_date(schedule.date)).id,
        lesson_id = (await add_discipline(value = schedule.discipline)).id,
        type_id = (await add(DBType, value = schedule.type)).id,
        auditorium_id = (await add(DBAuditorium, value = schedule.auditorium)).id,
        group_id = (await DBGroups.add(group = schedule.group)),
        teacher_id = (await DBTeacher.add(teacher = schedule.teacher)),
    )