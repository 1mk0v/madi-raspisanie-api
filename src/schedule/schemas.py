from models import Lesson, Group, Teacher

class Schedule(Lesson):
    weekday:str
    group: Group | None = None
    teacher: Teacher | None = None