from typing import List
from sqlalchemy import Table
from database.database import db
from models import Essence
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

    def _isEmpty(self, object):
        if (type(object) == list and len(object) == 0) \
            or (type(object) == dict and object == dict()) \
            or (type(object) == int and object == 0) \
            or (object == None):
            raise ValueError('The are no elements in table')
        return object

    async def _getValue(self, schema:Table, columnName:str, elementName:str, element, columnNumber:int = 1):
        return await self.db.fetch_val(
            query = schema.select().where(schema.c[columnName] == element[elementName]),
            column=columnNumber
        )

    async def getAll(self) -> List[BaseModel]:
        query = self.schema.select()
        return self._isEmpty(await db.fetch_all(query))
    
    async def getByColumn(self, columnName:str, columnValue:int | str ) -> List[BaseModel]:
        query = self.schema.select().where(self.schema.c[columnName] == columnValue)
        return self._isEmpty(await db.fetch_all(query))
    
    async def getById(self, id:int):
        query = self.schema.select().where(self.schema.c['id'] == id)
        return self._isEmpty(await db.fetch_one(query))
    
    async def add(self, model:Essence) -> BaseModel:
        query = self.schema.insert().values(id=model.id, value=model.value)
        return self._isEmpty(await db.execute(query))

    async def delete(self, id:int) -> int():
        query = self.schema.delete().where(self.schema.c['id'] == id)
        return await db.execute(query)