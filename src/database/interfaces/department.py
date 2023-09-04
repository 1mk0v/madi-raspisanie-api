from . import Interface
from models import Department
from database.schemas import department


class DepartmentDB(Interface):
    pass

DBDepartment = DepartmentDB(
    model=Department,
    schema=department
    )


