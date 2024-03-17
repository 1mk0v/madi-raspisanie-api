from .database import sync_engine
from sqlalchemy import (
    String, Time, ForeignKey, Integer
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, relationship, mapped_column
)
from typing import List
import datetime

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))

class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"), nullable=True)
    value: Mapped[str] = mapped_column(String(100))

class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"), nullable=True)
    value: Mapped[str] = mapped_column(String(100))

class EventDetailType(Base):
    __tablename__ = "event_detail_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(40))

class EventDetail(Base):
    __tablename__ = "event_detail"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('event_detail_type.id'))
    value: Mapped[str] = mapped_column(String(40))

class Time(Base):
    __tablename__ = "time"

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime.time] = mapped_column(Time) 
    end: Mapped[datetime.time] = mapped_column(Time, nullable=True)

class Event(Base):
    __tablename__="event"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(15), nullable=True)
    frequency_id: Mapped[str] = mapped_column(ForeignKey("event_detail.id"), nullable=True)
    time_id: Mapped[int] = mapped_column(ForeignKey("time.id"), nullable=True)
    time: Mapped["Time"] = relationship()
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), nullable=True)
    weekday_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"), nullable=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    auditorium_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"), nullable=True)

Base.metadata.drop_all(sync_engine)
Base.metadata.create_all(sync_engine)