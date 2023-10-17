from typing import List
from pydantic import BaseModel
import datetime

class Essence(BaseModel):
    id:int | None = None
    value:str | None = None 

class Group(Essence):
    department_id:int | None = None

class Teacher(Essence):
    department_id:int | None = None

class Time(BaseModel):
    start:datetime.time | None = None
    end:datetime.time | None = None

class Date(BaseModel):
    day:str | None = None
    friequency: str | None = None
    time:Time | None = None

class Lesson(BaseModel):
    date:Date
    discipline:str | List = None
    type:str | None = None
    auditorium:str | None = None

class Schedule(Lesson):
    group:Group | None = None
    teacher:Teacher | None = None

class LessonInfo(Schedule):
    weekday:str | None = None

class Response(BaseModel):
    statusCode:int
    detail:str = 'Success'
    data: str | list | Essence | Group | Teacher | None = None