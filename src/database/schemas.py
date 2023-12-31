from sqlalchemy import Column, Integer, String, Table, ForeignKey, Time
import databases
from sqlalchemy import  MetaData, create_engine

DATABASE_URL = "sqlite:///./database/test.db"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

department = Table(
    "department",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String),
)

group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("department_id", Integer, ForeignKey("department.id"), default = None),
    Column("value", String),
    Column("year", Integer)
)

teacher = Table(
    "teacher",
    metadata,
    Column("id", Integer, primary_key=True, unique = True),
    Column("department_id", Integer, ForeignKey("department.id"), default = None),
    Column("value", String),
    Column("year", Integer)
)

weekday = Table(
    "weekday",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("value", String, unique=True)
)

discipline = Table(
    "discipline",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("value", String, unique=True)
)

type = Table(
    "type",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("value", String, unique=True)
)

frequency = Table(
    "frequency",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("value", String, unique=True)
)

auditorium = Table(
    "auditorium",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("department_id", Integer, ForeignKey("department.id"), default = None),
    Column("value", String, unique=True)
)

time = Table(
    "time",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("start", Time , unique=True),
    Column("end", Time, unique=True)
)

date = Table(
    "date",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("day", String, default= None),
    Column("frequency_id", Integer, ForeignKey("frequency.id"), default= None),
    Column("time_id", Integer, ForeignKey("time.id"), default= None)
)

schedule = Table(
    "schedule_info",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("group_id",Integer, ForeignKey("group.id"), default= None),
    Column("teacher_id", Integer, ForeignKey("teacher.id"), default= None),
    Column("weekday_id", Integer, ForeignKey("weekday.id")),
    Column("date_id", Integer, ForeignKey("date.id"), default = None),
    Column("discipline_id", Integer, ForeignKey("discipline.id"), default = None),
    Column("type_id", Integer, ForeignKey("type.id"), default = None),
    Column("auditorium_id", Integer, ForeignKey("auditorium.id"), default= None)
)

exam = Table(
    "exam_info",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("group_id",Integer, ForeignKey("group.id"), default= None),
    Column("teacher_id", Integer, ForeignKey("teacher.id"), default= None),
    Column("date_id", Integer, ForeignKey("date.id"), default = None),
    Column("discipline_id", Integer, ForeignKey("discipline.id"), default = None),
    Column("type_id", Integer, ForeignKey("type.id"), default = None),
    Column("auditorium_id", Integer, ForeignKey("auditorium.id"), default= None)
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)