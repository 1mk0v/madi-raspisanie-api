from . import Interface
from .time import TimeDatabaseInterface
import models
import database.schemas as schemas

class DateDatabaseInterface(Interface):

    def __init__(self, model = models.Date, schema = schemas.date) -> None:
        super().__init__(model, schema)
        self.frequency = Interface(models.Essence, schemas.frequency) 
        self.time = TimeDatabaseInterface()
        
    async def getByValues(self, day:str, frequency_id:int, time_id:int):
        query = self.schema.select().where(
            self.schema.c.day == day,
            self.schema.c.frequency_id == frequency_id,
            self.schema.c.time_id == time_id,
        )
        return self._isEmpty(await self.db.fetch_one(query=query))

    async def add(self, day:str, frequency_id:int, time_id:int):
        query = self.schema.insert().values(
            day = day,
            frequency_id = frequency_id,
            time_id = time_id
        )
        return self._isEmpty(await self.db.execute(query=query))