from . import Interface
from MADI.models import Schedule
from database.schemas import schedule_info

class ScheduleDB(Interface):
    
    async def add():
        pass

    async def add_list():
        pass
    

DBSchedule = ScheduleDB(
    model=Schedule,
    schema=schedule_info
)