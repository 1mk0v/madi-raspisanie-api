from .config import *
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase

SYNC_DB_URL = f"postgresql+pg8000://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
        async with self.engine.connect() as conn:
            return await conn.execute(query)
         
    async def get(self):
        try:
            query = select(self.table)
            return await self.execute_query(query)
        except Exception as error:
            print(error)