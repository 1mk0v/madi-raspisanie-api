from pydantic import BaseModel


class Department(BaseModel):
    id: int
    name: str


class Group(BaseModel):
    id: int
    department_id: int
    name: str


class Teacher(BaseModel):
    id: int
    department_id: int
    name: str

class Event(BaseModel):
    group_id: int
    department_id: int
    name: str    