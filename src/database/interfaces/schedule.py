from . import Interface
from typing import List, Dict
from sqlalchemy import Table 
from models import (
    Date as Date_Model,
    Time as Time_Model,
    Teacher,
    Group
)
from groups.schemas import Schedule as Schedule_Group
from database.models import All_Schedule
from database.schemas import *

class ScheduleInfoDB(Interface):

    async def __get_value(self, schema:Table, col_name:str, el_name:str, element, col_num:int = 1):
        res = await self.db.fetch_val(query=schema.select().where(schema.c[col_name] == element[el_name]),
                                      column=col_num)
        return res
        
    async def format(self,data:List):
        #TODO - need optimization
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
            yield [weekday_info, All_Schedule(
                date=Date_Model(
                    day=date_info['day'],
                    friequency=frequency_info,
                    time = None if time_info == None else Time_Model(
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
            )]
    
    async def get_by_group(self, id:int) -> Dict[str, List[Schedule_Group]]:
        data = await self.get_by_column('group_id', id)
        schedule:Dict[str, List[Schedule_Group]] = dict()
        weekday:str = ''
        async for element in self.format(data=data):
            if weekday != element[0]:
                weekday = element[0]
                schedule[weekday] = list()
            schedule[weekday].append(
                Schedule_Group(
                    date=element[1].date,
                    discipline=element[1].discipline,
                    type=element[1].type,
                    auditorium=element[1].auditorium,
                    teacher=element[1].teacher
                ))
        return schedule
                

    async def get_by_teacher(self, id:int):
        data = await self.get_by_column('teacher_id', id)
        schedule:Dict[str, List[Schedule_Group]] = dict()
        weekday:str = ''
        async for element in self.format(data=data):
            if weekday != element[0]:
                weekday = element[0]
                schedule[weekday] = list()
            schedule[weekday].append(
                Schedule_Group(
                    date=element[1].date,
                    discipline=element[1].discipline,
                    type=element[1].type,
                    auditorium=element[1].auditorium,
                    group=element[1].group
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