from pydantic import BaseModel

class Response_Message(BaseModel):
    id:int | None = None
    detail:str = "Success"

class Exam(BaseModel):
    date_id:int | None = None
    lesson_id:int | None = None
    type_id:int | None = None
    auditorium_id:int | None = None
    teacher_id:int | None = None
    group_id:int | None = None

class Schedule(Exam):
    weekday_id:int | None = None
    