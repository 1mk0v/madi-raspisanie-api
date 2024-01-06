from sqlalchemy import Table
from . import Interface
from utils import get_current_year
from pydantic import BaseModel
from models import Community
from typing import List

class AcademicCommunityDatabaseInterface(Interface):
    """
        Actions with teacher or group database tables
    """
    def __init__(self, model:Community=Community, schema:Table = None) -> None:
        super().__init__(model, schema)

    async def getByRowId(self, id):
        data:Community = await self.getById(id)
        return self.model(
            id = data.id,
            value = data.value,
            department_id = data.department_id
        )

    async def getActual(self) -> List[Community]:
        query = self.schema.select().where(self.schema.c.year == get_current_year())
        data = self._getObjectOrRaiseError(await self.db.fetch_all(query))
        return [Community(**element) for element in data] 

    async def getByValue(self, value) -> BaseModel:
        query = self.schema.select().where(self.schema.c.value == value)
        return self._getObjectOrRaiseError(await self.db.fetch_one(query))

    async def add(self, community:BaseModel) -> BaseModel:
        if community == None:
            return None
        try:
            return (await self.getByValue(community.value)).id
        except:
            query = self.schema.insert().values(
                id = community.id,
                value = community.value,
                department_id = community.department_id,
                year = get_current_year()
            )
            return self._getObjectOrRaiseError(await self.db.execute(query))