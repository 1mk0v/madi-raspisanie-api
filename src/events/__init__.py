from sqlalchemy import select
from sqlalchemy.orm import aliased
from database import database, schemas

class EventsTableInterface(database.DatabaseInterface):

    def __init__(
            self,
            table: schemas.Event = schemas.Event,
            engine: database.AsyncEngine = database.async_engine
    ) -> None:
        super().__init__(table, engine)

    @property
    def base_query(self):
        return select(
            self.table.date,
            self.table.weekday,
            self.table.time_start.label('start'),
            self.table.time_end.label('end'),
            select(schemas.Frequency.value).where(schemas.Frequency.id == self.table.frequency_id).label('frequency'),
            select(schemas.EventType.value).where(schemas.EventType.id == self.table.type_id).label('type'),
            select(schemas.Auditorium.value).where(schemas.Auditorium.id == self.table.auditorium_id).label('auditorium'),
            select(schemas.Discipline.value).where(schemas.Discipline.id == self.table.discipline_id).label('discipline')
        ).where(self.table.is_deleted == 0)
    
    async def get_by_group_id(self, group_id):
        try:
            return await self._execute_query(self.base_query.where(self.table.group_id == group_id))
        except Exception as err:
            print(err)

    async def get_by_type(self, type_value:str=''):
        pass