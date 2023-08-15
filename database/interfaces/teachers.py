from . import Interface
from MADI.models import Teacher
from database.schemas import teacher


class TeacherDB(Interface):
    pass

DBTeacher = TeacherDB(
    model=Teacher,
    schema=teacher
)