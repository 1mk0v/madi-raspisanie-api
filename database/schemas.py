from sqlalchemy import Column, Integer, Boolean, String, Table, ForeignKey, Time
from typing import List
import databases
from .models import *
from sqlalchemy import  MetaData, create_engine

DATABASE_URL = "sqlite:///./database/test.db"

# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

department = Table(
    "department",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("value", String),
)

group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("department_id", Integer, ForeignKey("department.id"), default= None),
    Column("value", String),
)

teacher = Table(
    "teacher",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("department_id", Integer, ForeignKey("department.id"), default= None),
    Column("value", String),
)

weekday = Table(
    "weekday",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("value", String, unique=True)
)

discipline = Table(
    "discipline",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("value", String, unique=True)
)

type = Table(
    "type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("value", String, unique=True)
)

frequency = Table(
    "frequency",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("value", String, unique=True)
)

auditorium = Table(
    "auditorium",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("department_id", Integer, ForeignKey("department.id"), default = None),
    Column("value", String, unique=True)
)

time = Table(
    "time",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("start", Time , unique=True),
    Column("end", Time, unique=True)
)

date = Table(
    "date",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("day", String, default= None),
    Column("frequency_id", Integer, ForeignKey("frequency.id"), default= None),
    Column("time_id", Integer, ForeignKey("time.id"), default= None)
)

schedule_info = Table(
    "schedule_info",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("weekday_id", Integer, ForeignKey("weekday.id")),
    Column("date_id", Integer, ForeignKey("date.id")),
    Column("discipline_id", Integer, ForeignKey("discipline.id")),
    Column("type_id", Integer, ForeignKey("type.id")),
    Column("auditorium_id", Integer, ForeignKey("auditorium.id"), default= None)
)

exam_info = Table(
    "exam_info",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement="auto", unique=True),
    Column("date_id", Integer, ForeignKey("date.id")),
    Column("discipline_id", Integer, ForeignKey("discipline.id")),
    Column("auditorium_id", Integer, ForeignKey("auditorium.id"))
)

schedule = Table(
    "schedule",
    metadata,
    Column("schedule_id", Integer, ForeignKey("schedule_info.id")),
    Column("group_id", Integer, ForeignKey("group.id"))
)

exam = Table(
    "exam",
    metadata,
    Column("id", Integer, ForeignKey("exam.id")),
    Column("group_id", Integer, ForeignKey("group.id"))
)

metadata.create_all(engine)