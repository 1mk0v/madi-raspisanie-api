from sqlalchemy import select
from sqlalchemy.orm import aliased, joinedload, selectinload, subqueryload
from database import database, schemas

class EventsTableInterface(database.DatabaseInterface):

    def __init__(
            self,
            table: database.DeclarativeBase = schemas.Event,
            engine: database.AsyncEngine = database.async_engine
    ) -> None:
        super().__init__(table, engine)

    async def get_by_type(self, type_value:str=''):
        """
        select 
            event.date, 
            (select event_detail.value from event_detail where id = event.frequency_id) as frequency,
            (select event_detail.value from event_detail where id = event.weekday_id) as weekday,
            (select event_detail.value from event_detail where id = event.discipline_id) as discipline, 
            (select event_detail.value from event_detail where id = event.type_id) as type, 
            (select event_detail.value from event_detail where id = event.auditorium_id) as auditorium, 
            (select time.start from "time" where id = event.time_id) as time_start, 
            (select time.end from "time" where id = event.time_id) as time_end
        from event;
        """
        e = aliased(schemas.Event)
        ed = aliased(schemas.EventDetail)
        subquery = (
            select(
                e.date,
                select(ed.value).where(ed.id == e.frequency_id).label('frequency'),
                select(ed.value).where(ed.id == e.weekday_id).label('weekday'),
                select(ed.value).where(ed.id == e.discipline_id).label('discipline'),
                select(ed.value).where(ed.id == e.type_id).label('type'),
                select(ed.value).where(ed.id == e.auditorium_id).label('auditorium'),
                # select(schemas.Group).where(e.group_id == schemas.Group.id).subquery('group'),
                # select(schemas.Teacher).where(e.teacher_id == schemas.Teacher.id).subquery('teacher'),
                # select(schemas.EventTime.start, schemas.EventTime.end).where(ed.id == e.event_time_id).subquery()
            ).subquery('lesson_info')
        )
        query = select(subquery).where(subquery.c['type'] == type_value) 
        return await self.execute_query(query)