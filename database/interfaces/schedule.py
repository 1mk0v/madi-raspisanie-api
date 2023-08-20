from . import Interface
from MADI.models import Schedule_Info
from database.schemas import schedule_info

class ScheduleInfoDB(Interface):

    async def add(
        week_id:int,
        date_id:int,
        discipline_id:int #TODO
    ):
        #TODO
        pass

    async def add_list():
        pass
    

DBScheduleInfo = ScheduleInfoDB(
    model=Schedule_Info,
    schema=schedule_info
)