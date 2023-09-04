from . import Interface
from models import Time
from database.schemas import time
import datetime

class TimeDB(Interface):
    
    async def get_one(self, start:datetime.time, end:datetime.time):
        query = self.schema.select().where((self.schema.c.start == start) &
                                           (self.schema.c.end == end))
        return self._is_Empty(await self.db.fetch_one(query))
    
    async def add(self, start:datetime.time, end:datetime.time):
        query = self.schema.insert().values(start=start, end=end)
        return self._is_Empty(await self.db.execute(query))
    
    async def add_list(self):
        pass

DBTime = TimeDB(
    model=Time,
    schema=time
)