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


    async def _is_Empty(object):
        """
        Проверка исключений
        """ #TODO - проверка исключений на
        pass


    async def get_all(self) -> List[BaseModel]:
        query = self.schema.select()
        return await db.fetch_all(query)
    
    
    async def add(self, name:str, id:int = None) -> BaseModel:
        query = self.schema.insert().values(id=id, name=name)
        last_record_id = await db.execute(query)
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