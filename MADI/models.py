
from typing import Dict, List
from pydantic import BaseModel
import datetime

class Essence(BaseModel):
    id:int | None = None
    value:str | None = None 

class Department(Essence):
    pass

class Group(Essence):
    department_id:int | None = None

class Teacher(Essence):
    department_id:int | None = None

class Time(BaseModel):
    start:datetime.time
    end:datetime.time | None = None

class Date(BaseModel):
    day:str | None = None
    friequency: str | None = None
    time:Time | None = None

class Schedule(BaseModel):
    date:Date
    discipline:str | List = None
    type:str | None = None
    auditorium:str | None = None

class Schedule_Teacher(Schedule):
    group:Group

class Schedule_Group(Schedule):
    teacher:Teacher | None = None

class Schedule_Teacher_Info(BaseModel):
    teacher_info: Teacher | None = None
    schedule: Dict[str, List[Schedule_Teacher]]

class Schedule_Group_Info(BaseModel):
    group_info: Group | None = None
    schedule: Dict[str, List[Schedule_Group]]

class Exam_Teacher_Info(BaseModel):
    teacher_info: Teacher | None = None
    exam: List[Schedule]

class Exam_Group_Info(BaseModel):
    group_info:  Group | None = None
    exam: List[Schedule_Group]