from models import Lesson, Group, Teacher

class Schedule(Lesson):
    weekday:str | None = None
    group: Group | None = None
    teacher: Teacher | None = None