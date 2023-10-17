from pydantic import BaseModel
from . import Interface
from .academic_community import AcademicCommunityDatabaseInterface
from .date import DateDatabaseInterface
from .time import TimeDatabaseInterface
import models
import database.schemas as schemas


class ExamDatabaseInterface(Interface):
    
    def __init__(self, model = models.Schedule, schema = schemas.exam) -> None:
        super().__init__(model, schema)
        self.department = Interface(models.Essence, schemas.department)
        self.weekday = Interface(models.Essence, schemas.weekday)
        self.discipline = Interface(models.Essence, schemas.discipline) 
        self.type = Interface(models.Essence, schemas.type) 
        self.frequency = Interface(models.Essence, schemas.frequency) 
        self.auditorium = Interface(models.Essence, schemas.auditorium)
        self.date = DateDatabaseInterface()
        self.time = TimeDatabaseInterface()
        self.teacher = AcademicCommunityDatabaseInterface(models.Teacher, schemas.teacher)
        self.group = AcademicCommunityDatabaseInterface(models.Group, schemas.group)
    
    async def getByValues(self, model):
        pass

    async def getByGroupId(self, id:int):
        pass

    async def getByTeacherId(self, id:int):
        pass

    async def add(self, model:BaseModel):
        pass