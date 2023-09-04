from models import Lesson, Group, Teacher
# from pydantic import BaseModel



class Schedule(Lesson):
    weekday:str
    group: Group | None = None
    teacher: Teacher | None = None