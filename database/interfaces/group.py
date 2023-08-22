from . import Interface
from typing import List 
from MADI.models import Group
from MADI.main import get_current_year
from pydantic import BaseModel
from database.schemas import group, schedule


class GroupsDB(Interface):

    async def get_by_value_and_year(self, value:str) -> BaseModel:
        query = self.schema.select().where(self.schema.c.value == value,
                                           self.schema.c.year == get_current_year())
        return self._is_Empty(await self.db.fetch_one(query))

    async def get_schedule(self, id) -> List[BaseModel]:
        query = schedule.select().where(schedule.c.group_id == id)
        return self._is_Empty(await self.db.fetch_all(query))
    
    async def add(self, value:str, department_id:int = None, id:int = None) -> BaseModel:
        query = self.schema.insert().values(
            id = id,
            value = value,
            department_id = department_id,
            year = get_current_year())
        return self._is_Empty(await self.db.execute(query))
    

DBGroups = GroupsDB(
    model=Group,
    schema=group
    )


