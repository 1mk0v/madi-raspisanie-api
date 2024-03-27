from .config import *
from .schemas import Base
from exceptions import BaseServerException
from sqlalchemy import create_engine, select, CursorResult
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import exc as SQLException
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

SYNC_DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sync_engine = create_engine(
    SYNC_DB_URL
)
async_engine = create_async_engine(
    ASYNC_DB_URL, pool_recycle=3600
)

from .schemas import Base
class DatabaseInterface():
    
    def __init__(self, table:DeclarativeAttributeIntercept | Base, engine:AsyncEngine) -> None:
        self.table = table
        self.engine = engine

    async def _execute_query(self, query) -> CursorResult:
        try:
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except SQLException as error:
            print(error)
            raise BaseServerException()
        finally:
            await conn.close()

    @property
    def base_query(self):
        return select(self.table).where(self.table.is_deleted == 0)
    
    async def get(self) -> CursorResult:
        return await self._execute_query(self.base_query)


def create_database(drop_db:bool = False):
    if drop_db: Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)