from pydantic import BaseModel
from . import Interface
from .time import TimeDatabaseInterface
import models
import database.schemas as schemas

class DateDatabaseInterface(Interface):

    def __init__(self, model = models.Date, schema = schemas.date) -> None:
        super().__init__(model, schema)
        self.frequency = Interface(models.Essence, schemas.frequency) 
        self.time = TimeDatabaseInterface()

    class DateDatabaseModel(BaseModel):
        day:str
        frequency_id:int
        time_id:int

    async def getByRowId(self, id):
        data:self.DateDatabaseModel = await self.getById(id)
        frequencyValue = await self.frequency.getById(data.frequency_id)
        timeValue = await self.time.getByRowId(data.time_id)
        return self.model(
            day = data.day,
            frequency = (frequencyValue if frequencyValue != None else None),
            time = (timeValue if timeValue != None else None)
        )
        
    async def getByValues(self, date:DateDatabaseModel):
        query = self.schema.select().where(
            (self.schema.c.day == date.day) &
            (self.schema.c.frequency_id == date.frequency_id) &
            (self.schema.c.time_id == date.time_id)
        )
        return self._getObjectOrRaiseError(await self.db.fetch_one(query))

    async def add(self, date:models.Date):
        try:
            newDate = self.DateDatabaseModel(
                day = date.day,
                frequency_id=(await self.frequency.getByColumn('value', date.friequency))[0].id,
                time_id=(await self.time.getByValue(date.time)).id
            )
            return (await self.getByValues(newDate)).id
        except:
            query = self.schema.insert().values(
                day = date.day,
                frequency_id = await self.frequency.add(date.friequency),
                time_id = await self.time.add(date.time)
            )
            return self._getObjectOrRaiseError(await self.db.execute(query=query))