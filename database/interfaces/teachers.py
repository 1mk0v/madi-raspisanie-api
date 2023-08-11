from . import Main
from database.schemas import teacher
from MADI.models import Teacher

class TeacherDB(Main):
    pass

DBTeacher = TeacherDB(
    model=Teacher,
    schema=teacher
)