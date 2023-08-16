from . import Interface
from MADI.models import Schedule
from database.schemas import (
    schedule_info,
    date,
    time)

class ScheduleInfoDB(Interface):
    
    async def add(data:Schedule):
        print(time.select().where(time.c.start == data.date.time.start))
        pass

    async def add_list():
        pass
    

DBSchedule = ScheduleInfoDB(
    model=Schedule,
    schema=schedule_info
)