from . import Interface
from pydantic import BaseModel
from MADI.models import Teacher
from MADI.main import get_current_year
from database.schemas import teacher


class TeacherDB(Interface):
    async def add(self, value:str, department_id:int = None, id:int = None) -> BaseModel:
        query = self.schema.insert().values(
            id = id,
            value = value,
            department_id = department_id,
            year = get_current_year())
        return self._is_Empty(await self.db.execute(query))


DBTeacher = TeacherDB(
    model=Teacher,
    schema=teacher
)