from typing import List
from sqlalchemy import Table
from database.database import db
from pydantic import BaseModel

class Interface():

    def __init__(
            self,
            model:BaseModel,
            schema:Table
            ) -> None:
        self.model = model
        self.schema = schema
        self.db = db

    def _is_Empty(self, object):
        if (type(object) == list and len(object) == 0) \
            or (type(object) == dict and object == dict()) \
            or (type(object) == int and object == 0) \
            or (object == None):
            raise ValueError('The are no elements in table')
        return object

    async def get_all(self) -> List[BaseModel]:
        query = self.schema.select()
        return self._is_Empty(await db.fetch_all(query))
    
    async def get_by_column(self, column_name:str, column_value:int | str ) -> List[BaseModel]:
        query = self.schema.select().where(self.schema.c[column_name] == column_value)
        return self._is_Empty(await db.fetch_all(query))
    
    async def add(self, value:str, id:int = None) -> BaseModel:
        query = self.schema.insert().values(id=id, value=value)
        return self._is_Empty(await db.execute(query))

    async def delete(self, id:int) -> int():
        query = self.schema.delete().where(self.schema.c.id == id)
        return await db.execute(query)