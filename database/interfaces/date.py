from typing import Any, Coroutine, Dict, List
from pydantic import BaseModel
from pydantic.main import BaseModel
from . import Interface
from MADI.models import Date
from database.schemas import date


class DateDB(Interface):
    
    async def add(self):
        pass
    
    async def add_list(self):
        pass

DBTeacher = DateDB(
    model=Date,
    schema=date
)