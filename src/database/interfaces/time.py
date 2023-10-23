from . import Interface
from models import Time
from database.schemas import time

class TimeDatabaseInterface(Interface):
    
    def __init__(self, model = Time, schema = time) -> None:
        super().__init__(model, schema)
    
    async def getByRowId(self, id):
        data = await self.getById(id)
        return self.model(
            start = data.start,
            end = data.end
        )
    
    async def getByValue(self, time:Time):
        query = self.schema.select().where(
            (self.schema.c.start == time.start) &
            (self.schema.c.end == time.end)
        )
        return self._isEmpty(await self.db.fetch_one(query))
    
    async def add(self, time:Time):
        try:
            return (await self.getByValue(time)).id
        except:
            query = self.schema.insert().values(start=time.start, end=time.end)
            return self._isEmpty(await self.db.execute(query))