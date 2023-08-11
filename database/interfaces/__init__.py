from typing import List,Dict
from sqlalchemy import Table
from database.database import db

from pydantic import BaseModel

class Main():

    def __init__(
            self,
            model:BaseModel,
            schema:Table
            ) -> None:
        self.model = model
        self.schema = schema
        

    async def get_all(self) -> List[BaseModel]:
        query = self.schema.select()
        return await db.fetch_all(query)
    
    
    async def add(self, name:str) -> BaseModel:
        query = self.schema.insert().values(name=name)
        last_record_id = await db.execute(query)
        return self.model(id=last_record_id, value=name)
    
    
    async def add_list(self, list:List[Dict]):
        query = self.schema.insert()
        return await db.execute_many(query, list)

    
    async def delete(self, id:int) -> int():
        query = self.schema.delete().where(self.schema.c.id == id)
        return await db.execute(query)
        

    def update() -> BaseModel:
        pass


# from abc import ABC, abstractmethod

# class AbstractDBClass(ABC):

#     @abstractmethod
#     def get_all():
#         pass

#     @abstractmethod
#     def get_one():
#         pass

#     @abstractmethod
#     def add():
#         pass

#     @abstractmethod
#     def delete():
#         pass
    
#     @abstractmethod
#     def replace():
#         pass


# class GroupsDB(AbstractDBClass):

#     """
#     Methods for Groups with DB
#     """
    
#     @staticmethod
#     async def get_all() -> List[Group_Model]:
#         query = group.select()
#         return await db.fetch_all(query)
    
#     @staticmethod
#     async def add(name:str) -> Group_Model:
#         query = group.insert().values(name=name)
#         last_record_id = await db.execute(query)
#         return Group_Model(id=last_record_id, value=name)
    
#     @staticmethod
#     async def add_list(list:List[Dict]):
#         query = group.insert()
#         return await db.execute_many(query, list)

#     @staticmethod
#     async def delete(id:int) -> int():
#         query = group.delete().where(group.c.id == id)
#         return await db.execute(query) 
        
#     @staticmethod
#     def update() -> Group_Model:
#         pass