from schedule.schemas import Schedule
from pydantic import BaseModel

class Response_Message(BaseModel):
    id:int | None = None
    detail:str = "Success"

class Schedule_Info(BaseModel):
    weekday_id:int | None = None
    date_id:int | None = None
    lesson_id:int | None = None
    type_id:int | None = None
    frequency_id:int | None = None
    auditorium_id:int | None = None
    teacher_id:int | None = None
    group_id:int | None = None

class All_Schedule(Schedule):
    pass