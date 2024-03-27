from sqlalchemy import select
from sqlalchemy.ext.asyncio import exc as SQLException
from database import database, schemas
from exceptions import BaseServerException

class EventsTableInterface(database.DatabaseInterface):

    def __init__(
            self,
            table: schemas.Event = schemas.Event,
            engine: database.AsyncEngine = database.async_engine
    ) -> None:
        super().__init__(table, engine)

    @property
    def base_query(self):
        return (
            select
            (
                self.table.date,
                self.table.weekday,
                self.table.time_start.label('start'),
                self.table.time_end.label('end'),
                select(schemas.Frequency.value).where(schemas.Frequency.id == self.table.frequency_id).label('frequency'),
                select(schemas.EventType.value).where(schemas.EventType.id == self.table.type_id).label('type'),
                select(schemas.Auditorium.value).where(schemas.Auditorium.id == self.table.auditorium_id).label('auditorium'),
                select(schemas.Discipline.value).where(schemas.Discipline.id == self.table.discipline_id).label('discipline'),
                schemas.Group.id.label('group_id'),
                schemas.Group.department_id.label('group_department_id'),
                schemas.Group.value.label('group_value'),
                schemas.Teacher.id.label('teacher_id'),
                schemas.Teacher.department_id.label('teacher_department_id'),
                schemas.Teacher.value.label('teacher_value')
            )
            .join(self.table.group)
            .join(self.table.teacher)
            .where(self.table.is_deleted == 0)
        )
    

    async def get_event_type_id(self, value):
        query = select(schemas.EventType.id).where(schemas.EventType.value == value)
        event_type_id = await self._execute_query(query)
        data = event_type_id.fetchone()
        return data[0] if data else None
    
    async def get_lessons_by_group_id(self, id):
        return await self._execute_query(
            self.base_query
                .where(self.table.type_id != (await self.get_event_type_id('Экзамен')))
                .where(self.table.group_id == id)
        )
    
    async def get_lessons_by_teacher_id(self, id):
        return await self._execute_query(
            self.base_query
                .where(self.table.type_id != (await self.get_event_type_id('Экзамен')))
                .where(self.table.teacher_id == id)
        )

    async def get_exam_by_group_id(self, id):
        return await self._execute_query(
            self.base_query
                .where(self.table.type_id == (await self.get_event_type_id('Экзамен')))
                .where(self.table.group_id == id)
        )
    
    async def get_exam_by_teacher_id(self, id):
        return await self._execute_query(
            self.base_query
                .where(self.table.type_id == (await self.get_event_type_id('Экзамен')))
                .where(self.table.teacher_id == id)
        )

    