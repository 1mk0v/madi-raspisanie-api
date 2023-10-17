from sqlalchemy import Table
from . import Interface
from utils import get_current_year
from pydantic import BaseModel

class AcademicCommunityDatabaseInterface(Interface):
    """
        Actions with teacher or group database tables
    """
    def __init__(self, model:BaseModel, schema:Table) -> None:
        super().__init__(model, schema)

    async def getActual(self) -> BaseModel:
        query = self.schema.select().where(self.schema.c.year == get_current_year())
        return self._isEmpty(await self.db.fetch_all(query))
    
    async def add(self, community:BaseModel) -> BaseModel:
        query = self.schema.insert().values(
            id = community.id,
            value = community.value,
            department_id = community.department_id,
            year = get_current_year()
        )
        return self._isEmpty(await self.db.execute(query))