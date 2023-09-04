from pydantic import BaseModel
from models import Lesson, Group, Teacher
from typing import Dict, List

class TeacherInfo(BaseModel):
    teacher: Teacher | None = None

class TeacherLesson(Lesson):
    group: Group | None = None

class Schedule(TeacherInfo):
    schedule: Dict[str, List[TeacherLesson]]

class Exam(TeacherInfo):
    exams: List[TeacherLesson]
