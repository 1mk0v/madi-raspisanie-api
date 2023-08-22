from . import Interface
from database.models import Schedule_Info
from database.schemas import schedule

class ScheduleInfoDB(Interface):

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