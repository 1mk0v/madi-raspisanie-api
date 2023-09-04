from . import Interface
from groups.schemas import Group
from utils import get_current_year
from pydantic import BaseModel
from database.schemas import group


class GroupsDB(Interface):

    async def get_actual(self):
        """
            Searching by current academic year
        """
        query = self.schema.select().where(self.schema.c.year == get_current_year())
        return self._is_Empty(await self.db.fetch_all(query))
    
    async def get(self, id:int | None, value:str) -> BaseModel:
        """
            Searching by value and current academic year
        """
        try:
            query = self.schema.select().where(self.schema.c.id == id)
            return self._is_Empty(await self.db.fetch_one(query))
        except ValueError:
            query = self.schema.select().where(self.schema.c.value == value,
                                               self.schema.c.year == get_current_year())
            return self._is_Empty(await self.db.fetch_one(query))
    
    async def add(self, value:str, department_id:int = None, id:int = None) -> BaseModel:
        if value == None: 
            raise ValueError("Can't add teacher without value")
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


