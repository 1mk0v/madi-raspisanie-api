
from typing import Dict, List
from pydantic import BaseModel


class Selectors(BaseModel):
    name: str
    value: str


class Date(BaseModel):
    #TODO - change types
    date:str | None = None
    friequency: str | None = None
    time:str



class Schedule_Info(BaseModel):
    date: Date
    discipline:str
    group:str | None = None
    teacher:str | None = None
    auditorium:str

class Schedule(BaseModel):
    week_day: str
    schedule: List[Schedule_Info]


class Info(BaseModel):
    selectors: Selectors
    schedule: Schedule
    