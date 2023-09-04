from . import Interface
from pydantic import BaseModel
from teachers.schemas import Teacher
from utils import get_current_year
from database.schemas import teacher


class TeacherDB(Interface):
    async def get_actual(self):
        query = self.schema.select().where(self.schema.c.year == get_current_year())
        return self._is_Empty(await self.db.fetch_all(query))
    
    async def add(self, teacher:Teacher) -> BaseModel:
        if teacher.value == None:
            raise ValueError("Can't add teacher without value")
        query = self.schema.insert().values(
            id = teacher.id,
            value = teacher.value,
            department_id = teacher.department_id,
            year = get_current_year())
        return self._is_Empty(await self.db.execute(query))


DBTeacher = TeacherDB(
    model=Teacher,
    schema=teacher
)