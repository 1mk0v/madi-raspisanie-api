from . import Interface
from typing import List
from MADI.models import Schedule, Date, Time, Schedule_Info
from .group import DBGroups
from .teachers import DBTeacher
from .department import DBDepartment
from .date import DBDate
from .frequency import DBFrequency
from .weekday import DBWeekday

import datetime
from database.schemas import (
    group,
    teacher,
    schedule_info,
    date,
    time)
from database.database import db

schedule = Schedule(
    date=Date(
        friequency='Еженедельно',
        time=Time(
            start=datetime.datetime.time(datetime.datetime.strptime('18:50','%H:%M')),
            end=datetime.datetime.time(datetime.datetime.strptime('20:20','%H:%M'))
            )
    ),
    group='2ВбАСУ',
    auditorium='605л'
)

my_data = Schedule_Info(
    name='Сальный А.Г.',
    schedule={
        "Понедельник": [
            schedule
        ]
    }
)

DBTablesMethods:List[Interface] = [DBTeacher, DBDate, DBDepartment, DBFrequency, DBGroups, DBWeekday]
class ScheduleInfoDB(Interface):

    async def add(data:Schedule_Info):
        for table in DBTablesMethods:
            await table
        await DBGroups.get_by_name(my_data.name)
        print(await db.fetch_all(time.select().where(time.c.start == my_data.schedule['Понедельник'][0].date.time.start)))

    async def add_list():
        pass
    

DBSchedule = ScheduleInfoDB(
    model=Schedule_Info,
    schema=schedule_info
)