from . import Interface
from models import Time
from database.schemas import time
import datetime

class TimeDatabaseInterface(Interface):
    
    def __init__(self, model = Time, schema = time) -> None:
        super().__init__(model, schema)
        
    async def getByValue(self, start:datetime.time, end:datetime.time):
        query = self.schema.select().where(
            (self.schema.c.start == start) &
            (self.schema.c.end == end)
        )
        return self._isEmpty(await self.db.fetch_one(query))
    
    async def add(self, start:datetime.time, end:datetime.time):
        query = self.schema.insert().values(start=start, end=end)
        return self._isEmpty(await self.db.execute(query))