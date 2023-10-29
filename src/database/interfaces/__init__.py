from typing import List
from sqlalchemy import Table
from database.database import db
from pydantic import BaseModel

class Interface():

    def __init__(self, model:BaseModel, schema:Table) -> None:
        self.model = model
        self.schema = schema
        self.db = db

    def _getObjectOrRaiseError(self, object):
        if (type(object) == list and len(object) == 0) \
            or (type(object) == dict and object == dict()) \
            or (type(object) == int and object == 0):
            raise ValueError('The are no elements in table')
        return object

    async def _getValue(self, schema:Table, columnName:str, elementName:str, element, columnNumber:int = 1):
        return await self.db.fetch_val(
            query = schema.select().where(schema.c[columnName] == element[elementName]),
            column=columnNumber
        )

    async def getAll(self) -> List[BaseModel]:
        query = self.schema.select()
        return self._getObjectOrRaiseError(await db.fetch_all(query))
    
    async def getByColumn(self, columnName:str, columnValue:int | str ) -> List[BaseModel]:
        query = self.schema.select().where(self.schema.c[columnName] == columnValue)
        return self._getObjectOrRaiseError(await db.fetch_all(query))

    async def getById(self, id:int):
        query = self.schema.select().where(self.schema.c['id'] == id)
        return self._getObjectOrRaiseError(await db.fetch_one(query))
    
    async def add(self, value:str) -> BaseModel:
        if value == None:
            return None
        try:
            return (await self.getByColumn('value', value))[0].id
        except:
            query = self.schema.insert().values(value=value)
            return self._getObjectOrRaiseError(await db.execute(query))

    async def delete(self, id:int) -> int():
        query = self.schema.delete().where(self.schema.c['id'] == id)
        return await db.execute(query)