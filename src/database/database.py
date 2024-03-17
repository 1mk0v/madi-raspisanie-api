from .config import *
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, select, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase

SYNC_DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
sync_engine = create_engine(
    SYNC_DB_URL, echo=True
)

ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
async_engine = create_async_engine(
    ASYNC_DB_URL, echo=True
)

class DatabaseInterface():
    
    def __init__(self, table:DeclarativeBase, engine:AsyncEngine) -> None:
        self.table = table
        self.engine = engine

    async def execute_query(self, query):
        try:
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except Exception as error:
            print(error)
        finally:
            await conn.close()
            
    async def execute_stmt(self, stmt):
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(stmt) 
                await conn.commit()
                return result
        except Exception as error:
            await conn.rollback()
        finally:
            await conn.close()

    async def get(self):
        try:
            query = select(self.table)
            return (await self.execute_query(query))
        except Exception as error:
            print(error)

    async def add(self, data:BaseModel | List[BaseModel]):
        try:
            values = [item.model_dump() for item in data] if type(data) == list else data.model_dump()
            stmt = insert(self.table).values(values).returning(self.table)
            return await self.execute_stmt(stmt)
        except Exception as error:
            print(error)