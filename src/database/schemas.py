from .database import sync_engine
from sqlalchemy import String, Time, ForeignKey, Integer, sql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
import datetime


intpk = Annotated[int, mapped_column(Integer, primary_key=True)]
boolInt = Annotated[int, mapped_column(Integer, insert_default=0, server_default='0')]
depfgnkey = Annotated[int, mapped_column(ForeignKey('department.id'), nullable=True)]

class Base(DeclarativeBase):
    id: Mapped[intpk]
    is_deleted: Mapped[boolInt]

class Department(Base):
    __tablename__ = "department"

    value: Mapped[str] = mapped_column(String(100))

class Teacher(Base):
    __tablename__ = "teacher"

    department_id: Mapped[depfgnkey]
    year: Mapped[int]
    value: Mapped[str] = mapped_column(String(100))

class Group(Base):
    __tablename__ = "group"

    department_id: Mapped[depfgnkey]
    year: Mapped[int]
    value: Mapped[str] = mapped_column(String(100))

class Discipline(Base):
    __tablename__ = "discipline"

    id:Mapped[intpk]
    value: Mapped[str] = mapped_column(String)
    department_id: Mapped[depfgnkey]

class Frequency(Base):
    __tablename__ = "frequency"

    id:Mapped[intpk]
    value: Mapped[str] = mapped_column(String)

class EventType(Base):
    __tablename__ = "event_type"

    id:Mapped[intpk]
    value: Mapped[str] = mapped_column(String)

class Auditorium(Base):
    __tablename__ = "auditorium"

    id:Mapped[intpk]
    value: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, nullable=True)
    is_reserved: Mapped[boolInt]

class Event(Base):
    __tablename__ = "event"

    date: Mapped[str] = mapped_column(String(15), nullable=True)
    frequency_id: Mapped[str] = mapped_column(ForeignKey('frequency.id'), nullable=True)
    time_start: Mapped[datetime.time] = mapped_column(Time)
    time_end: Mapped[datetime.time] = mapped_column(Time, nullable=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey('discipline.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('event_type.id'))
    auditorium_id: Mapped[int] = mapped_column(ForeignKey('auditorium.id'), nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), nullable=True)
    weekday: Mapped[str] = mapped_column(String(30),nullable=True)

# Base.metadata.drop_all(sync_engine)
Base.metadata.create_all(sync_engine)