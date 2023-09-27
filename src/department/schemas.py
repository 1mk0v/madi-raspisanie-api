from pydantic import BaseModel
from models import Essence, Schedule
from typing import Dict, List

class Department(Essence):
    pass

class DepartmentLesson(Schedule):
    pass

class DepartmentInfo(BaseModel):
    department: Department | None = None

class DepartmentSchedule(DepartmentInfo):
    schedule: Dict[str, List[Schedule]]
