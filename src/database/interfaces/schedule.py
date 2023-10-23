from . import Interface
from bridges.madi import LessonInfo
from .academic_community import AcademicCommunityDatabaseInterface
from .date import DateDatabaseInterface
import models
import database.schemas as schemas

class ScheduleDatabaseInterface(Interface):

    def __init__(self, model = LessonInfo, schema = schemas.schedule) -> None:
        super().__init__(model, schema)
        self.weekday = Interface(models.Essence, schemas.weekday)
        self.discipline = Interface(models.Essence, schemas.discipline)
        self.type = Interface(models.Essence, schemas.type)
        self.auditorium = Interface(models.Essence, schemas.auditorium)
        self.teacher = AcademicCommunityDatabaseInterface(schema=schemas.teacher)
        self.group = AcademicCommunityDatabaseInterface(schema=schemas.group)
        self.date = DateDatabaseInterface()

    class ScheduleDatabaseModel:
        id:int
        weekday_id:int
        date_id:int
        discipline_id:int
        type_id:int
        auditorium_id:int
        teacher_id:int
        group_id:int

    async def _getByRowId(self, row:ScheduleDatabaseModel):
        return self.model(
            date = (await self.date.getByRowId(row.date_id)),
            discipline = (await self.discipline.getById(row.discipline_id)).value,
            type = (await self.type.getById(row.type_id)).value,
            auditorium = (await self.auditorium.getById(row.auditorium_id)).value,
            teacher = (await self.teacher.getByRowId(row.teacher_id)),
            group = (await self.group.getByRowId(row.group_id)),
            weekday = (await self.weekday.getById(row.weekday_id)).value,
        )

    async def _generateResult(self, data):
        result = list()
        for row in data:
            result.append(await self._getByRowId(row))
        return result
    
    async def getByGroupId(self,id:int):
        query = self.schema.select().where(self.schema.c['group_id'] == id)
        data = self._isEmpty(await self.db.fetch_all(query))
        return await self._generateResult(data)

    async def getByTeacherId(self, id:int):
        query = self.schema.select().where(self.schema.c['teacher_id'] == id)
        data = self._isEmpty(await self.db.fetch_all(query))
        return await self._generateResult(data)

    async def add(self, schedule):
        data = {}
        for field in schedule:
            nameOfField = field[0]
            fieldData = field[1]
            databaseInterface:Interface = self.__dict__[nameOfField]
            data[f'{nameOfField}_id'] = await databaseInterface.add(fieldData)
        query = self.schema.insert().values(data)
        return self._isEmpty(await self.db.execute(query))
    

class ExaminationDatabaseInterface(ScheduleDatabaseInterface):

    def __init__(self, model=models.Schedule, schema=schemas.exam) -> None:
        super().__init__(model, schema)

    class ExamDatabaseModel:
        id:int
        date_id:int
        discipline_id:int
        type_id:int
        auditorium_id:int
        teacher_id:int
        group_id:int

    async def _getByRowId(self, row:ExamDatabaseModel):
        return self.model(
            date = (await self.date.getByRowId(row.date_id)),
            discipline = (await self.discipline.getById(row.discipline_id)).value,
            type = (await self.type.getById(row.type_id)).value,
            auditorium = (await self.auditorium.getById(row.auditorium_id)).value,
            teacher = (await self.teacher.getByRowId(row.teacher_id)),
            group = (await self.group.getByRowId(row.group_id)),
        )