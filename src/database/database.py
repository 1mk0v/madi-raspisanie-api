from .config import *
from sqlalchemy import create_engine, select, CursorResult
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import exc as SQLException
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

SYNC_DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sync_engine = create_engine(
    SYNC_DB_URL, echo=True
)
async_engine = create_async_engine(
    ASYNC_DB_URL, echo=True, pool_recycle=3600
)

from .schemas import Base
class DatabaseInterface():
    
    def __init__(self, table:DeclarativeAttributeIntercept | Base, engine:AsyncEngine) -> None:
        print(type(table))
        self.table = table
        self.engine = engine

    async def _execute_query(self, query) -> CursorResult:
        try:
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except SQLException as error:
            print(error)
        finally:
            await conn.close()

    @property
    def base_query(self):
        return select(self.table).where(self.table.is_deleted == 0)
    
    async def get(self) -> CursorResult:
        try:
            return await self._execute_query(self.base_query)
        except Exception as error:
            print(error)