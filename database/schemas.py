from sqlalchemy import Column, Integer, Boolean, String, Table, ForeignKey
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
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("department_id", Integer, ForeignKey("department.id")),
    Column("name", String),
)


teacher = Table(
    "teacher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("department_id", Integer, ForeignKey("department.id")),
    Column("name", String),
)


event = Table(
    "event",
    metadata,
    Column("group_id", Integer, primary_key=True),
    Column("schedule_id", Integer),
    Column("exam_id", Integer)
)


week_day = Table(
    "week_day",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String)
)


time = Table(
    "time",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String)
)


lesson = Table(
    "lesson",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)


schedule_type = Table(
    "schedule_type",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String)
)


frequency = Table(
    "frequency",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)


date = Table(
    "date",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String)
)


auditorium = Table(
    "auditorium",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("department_id", Integer, ForeignKey("department.id")),
    Column("value", String)
)



metadata.create_all(engine)