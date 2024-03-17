from typing import List, Any
from pydantic import BaseModel
import datetime

class Essence(BaseModel):
    id:int | None = None
    value:str | None = None 

class Community(Essence):
    department:str | None = None

class Time(BaseModel):
    start:datetime.time | None = None
    end:datetime.time | None = None

class Lesson(BaseModel):
    day:str | None = None
    friequency: str | None = None
    time:Time | None = None
    discipline:str | List = None
    type:str | None = None
    auditorium:str | None = None

class Schedule(Lesson):
    group:Community | None = None
    teacher:Community | None = None

class LessonInfo(Schedule):
    weekday:str | None = None

class Response(BaseModel):
    statusCode:int = 200
    detail:str = 'Success'
    data: List[Essence] | List[Community] | List[LessonInfo] | List[Any] | None = None

class ResponseWithCommunity(Response):
    data: List[Community]

class ResponseWithLessonInfo(Response):
    data: List[LessonInfo]