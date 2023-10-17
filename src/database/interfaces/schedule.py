from . import Interface
from pydantic import BaseModel
import database.interfaces as interfacesModule
from bridges.madi import LessonInfo
from database.database import db
from .academic_community import AcademicCommunityDatabaseInterface
from .date import DateDatabaseInterface
from .time import TimeDatabaseInterface
import models
import database.schemas as schemas

class ScheduleDatabaseInterface(Interface):

    def __init__(self, model = models.Schedule, schema = schemas.schedule) -> None:
        super().__init__(model, schema)
        self.department = Interface(models.Essence, schemas.department)
        self.weekday = Interface(models.Essence, schemas.weekday)
        self.discipline = Interface(models.Essence, schemas.discipline)
        self.type = Interface(models.Essence, schemas.type)
        self.frequency = Interface(models.Essence, schemas.frequency)
        self.auditorium = Interface(models.Essence, schemas.auditorium)
        self.date = DateDatabaseInterface()
        self.time = TimeDatabaseInterface()
        self.teacher = AcademicCommunityDatabaseInterface(models.Group, schemas.group)
        self.group = AcademicCommunityDatabaseInterface(models.Teacher, schemas.teacher)

    async def getByValues(self, model):
        pass

    async def getByGroupId(self,id:int):
        query = self.schema.select().where(self.schema.c['group_id'] == id)
        return self._isEmpty(await self.db.fetch_all(query))

    async def getByTeacherId(self, id:int):
        query = self.schema.select().where(self.schema.c['teacher_id'] == id)
        return self._isEmpty(await db.fetch_all(query))

    async def add(self, model):
        if type(model) != type(str()):
            for field in model:
                if issubclass(type(field[1]), BaseModel):
                    await self.add(field[1])
                else:
                    databaseTables = [key for key in self.__dict__ ]
                    print(databaseTables)
                    print(field)