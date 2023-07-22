
from typing import Dict, List
from pydantic import BaseModel, BaseConfig

class Time(BaseModel):
    start:str
    end:str

class Date(BaseModel):
    #TODO - change types
    day:str | None = None
    friequency: str | None = None
    time:str | None = None


class Schedule(BaseModel):
    date: Date
    discipline:str | List
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