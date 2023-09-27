from . import Interface
from groups.schemas import Group
from utils import get_current_year
from pydantic import BaseModel
from database import schemas 


class GroupsDB(Interface):

    async def get_actual(self):
        query = self.schema.select().where(self.schema.c.year == get_current_year())
        return self._is_Empty(await self.db.fetch_all(query))
    

    async def get(self, id:int | None, value:str) -> BaseModel:
        if id != None:
            query = self.schema.select().where(self.schema.c.id == id)
        else:
            query = self.schema.select().where(self.schema.c.value == value,
                                               self.schema.c.year == get_current_year())
        return self._is_Empty(await self.db.fetch_one(query))
    

    async def add(self, group:Group) -> BaseModel:
        if group.value == None: 
            raise ValueError("Can't add group without value")
        try:
            res = (await self.get_by_column('id', group.id))[0]
            return res.id
        except:
            query = self.schema.insert().values(
                id = group.id,
                value = group.value,
                department_id = group.department_id,
                year = get_current_year())
            return self._is_Empty(await self.db.execute(query))
    

DBGroups = GroupsDB(
    model=Group,
    schema=schemas.group
    )


