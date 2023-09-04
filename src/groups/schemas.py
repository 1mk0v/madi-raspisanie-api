from pydantic import BaseModel
from models import Lesson, Group, Teacher
from typing import Dict, List

class GroupLesson(Lesson):
    teacher: Teacher | None = None

class GroupInfo(BaseModel):
    group: Group | None = None

class Schedule(GroupInfo):
    schedule: Dict[str, List[GroupLesson]]

class Exam(GroupInfo):
    exams: List[GroupLesson]
