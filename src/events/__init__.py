from sqlalchemy import select
from sqlalchemy.orm import aliased
from database import database, schemas

class EventsTableInterface(database.DatabaseInterface):

    def __init__(
            self,
            table: database.DeclarativeBase = schemas.Event,
            engine: database.AsyncEngine = database.async_engine
    ) -> None:
        super().__init__(table, engine)

    """
    insert into event_detail_type (value) values ('Тип недели'),('Аудитория'),('Дисциплина'),('Тип события'),('День недели'); 
    insert into event_detail (type_id, value) values (1, 'Числитель'), (3, 'Тестовая дисциплина'), (4, 'Лекция'), (5, 'Понедельник'), (2, '234H');
    insert into "time" (start, "end") values ('18:50:00', '20:20:00'), ('20:30:00', '22:00:00'); 
    insert into "group" (id, value) values (1, 'Group1'), (2, 'Group2'), (3, 'Group3');
    insert into "teacher" (id, value) values (1, 'Teacher1'), (2, 'Teacher2'), (3, 'Teacher3');
    insert into event (date, frequency_id, discipline_id,group_id, teacher_id, time_id, type_id, weekday_id, auditorium_id) values ('', 1, 2, 1, 1, 1, 3, 4, 5); 
    """
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
        try:
            e = aliased(schemas.Event)
            ed = aliased(schemas.EventDetail)
            query = (
                select(
                    e.date,
                    select(ed.value).where(ed.id == e.frequency_id).subquery('frequency'),
                    select(ed.value).where(ed.id == e.weekday_id).subquery('weekday'),
                    select(ed.value).where(ed.id == e.discipline_id).subquery('discipline'),
                    select(ed.value).where(ed.id == e.type_id).subquery('type'),
                    select(ed.value).where(ed.id == e.auditorium_id).subquery('auditorium'),
                    # select(schemas.Time.start).where(schemas.Time.id == e.time_id).subquery('time_start'),
                    # select(schemas.Time.end).where(schemas.Time.id == e.time_id).subquery('time_end')
                )
            )
            print((await self.execute_query(query)).all())
            return None
        except Exception as error:
            print(error)