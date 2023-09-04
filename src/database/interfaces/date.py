from . import Interface
from models import Date
from database.schemas import date


class DateDB(Interface):
    
    async def get_one(self, day:str, frequency_id:int, time_id:int):
        query = self.schema.select().where(
            self.schema.c.day == day,
            self.schema.c.frequency_id == frequency_id,
            self.schema.c.time_id == time_id,
        )
        return self._is_Empty(await self.db.fetch_one(query=query))

    async def add(self, day:str, frequency_id:int, time_id:int):
        query = self.schema.insert().values(
            day=day,
            frequency_id=frequency_id,
            time_id=time_id
        )
        return self._is_Empty(await self.db.execute(query=query))
            
    async def get_model(self, DBobject):
        print(DBobject)
        for i in DBobject:
            print(i)


DBDate = DateDB(
    model=Date,
    schema=date
)