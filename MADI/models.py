
from typing import Dict, List
from pydantic import BaseModel
import datetime

class Essence(BaseModel):
    id:int
    value:str

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
    #TODO - change types
    day:str | None = None
    friequency: str | None = None
    time:Time | None = None


class Schedule(BaseModel):
    date: Date
    discipline:str | List = None
    type:str | None = None
    group:str | None = None 
    teacher:str | None = None
    auditorium:str | None = None


class Schedule_Info(BaseModel):
    name: str | None = None
    schedule: Dict[str, List[Schedule]]


class Exam_Info(BaseModel):
    name: str | None = None
    exam: List[Schedule] 