from typing import List,Dict
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError
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


    def _is_Empty(self, object):

        """
        Проверка исключений
        """
        if (type(object) == list and len(object) == 0) \
            or (type(object) == dict and object == dict()) \
            or (type(object) == int and object == 0):
            raise ValueError('The are no elements in table')

        return object


    async def get_all(self) -> List[BaseModel]:
        query = self.schema.select()
        return self._is_Empty(await db.fetch_all(query))


    async def add(self, name:str, id:int = None) -> BaseModel:
        query = self.schema.insert().values(id=id, name=name)
        last_record_id = self._is_Empty(await db.execute(query)) 
        return self.model(id=last_record_id, value=name)


    async def add_list(self, list:List[Dict]):
        query = self.schema.insert()
        return await db.execute_many(query, list)


    async def delete(self, id:int) -> int():
        """
        Returns:
            int: 1, if succesufully deleted
            int: 0, if not found 
        """
        query = self.schema.delete().where(self.schema.c.id == id)
        return await db.execute(query)


    async def update(self, id:int, column, text:str) -> BaseModel:
        pass