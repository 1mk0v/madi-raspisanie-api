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

class ScheduleInfoDB(Interface):

    async def __get_value(self, schema:Table, col_name:str, el_name:str, element, col_num:int = 1):
        res = await self.db.fetch_val(query=schema.select().where(schema.c[col_name] == element[el_name]),
                                      column=col_num)
        return res
        
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
            print(weekday_info)
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
            print(element)
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
            print(element)
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
        weekday_id:int,
        date_id:int,
        discipline_id:int,
        type_id:int,
        auditorium_id:int,
        teacher_id:int,
        group_id:int
    ):
        query = self.schema.insert().values(
            weekday_id=weekday_id,
            date_id=date_id,
            discipline_id=discipline_id,
            type_id=type_id,
            auditorium_id=auditorium_id,
            teacher_id = teacher_id,
            group_id = group_id)
        return self._is_Empty(await self.db.execute(query))
    

DBScheduleInfo = ScheduleInfoDB(
    model=Schedule_Info,
    schema=schedule
)