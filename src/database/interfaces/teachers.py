from sqlalchemy import Table
from . import Interface
from pydantic import BaseModel
from teachers.schemas import Teacher
from utils import get_current_year
from database.schemas import teacher
from models import ResponseMessage


class TeacherDB(Interface):

    def __init__(self, model: BaseModel, schema: Table) -> None:
        super().__init__(model, schema)
        
    async def get_actual(self):
        return await self.get_by_column(column_name='year', column_value = get_current_year())
    
    async def add(self, teacher:Teacher) -> BaseModel:
        if teacher.value == None:
            raise ValueError("Can't add teacher without value")
        try:
            res = (await self.get_by_column('id', teacher.id))[0]
            return res.id
        except:
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