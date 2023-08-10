from pydantic import BaseModel


class Department(BaseModel):
    id: int
    name: str


class Group(BaseModel):
    id: int
    department_id: int | None = None
    name: str


class Teacher(BaseModel):
    id: int
    department_id: int | None = None
    name: str


class Schedule(BaseModel):
    id:int
    department_id:int | None = None
    group_id:int

class Schedule_info(BaseModel):
    schedule_id:int
    week_day_id:str
    time_id:str
    lesson_id:str
    type_id:str
    frequency_id:str
    auditorium_id:str
    teacher_id:str

class Exam_info(BaseModel):
    exam_id:int
    date_id:str
    time_id:str
    lesson_id:str
    auditorium_id:str
    teacher_id:str


class Other(BaseModel):
    
    """
    Can be anything that has ID and Value
    """

    id:int
    value:str