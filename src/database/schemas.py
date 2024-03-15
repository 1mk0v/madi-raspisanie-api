from .database import sync_engine
from sqlalchemy import (
    String, Integer, Time, ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column
)
import datetime
class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))

class CommunityType(Base):
    __tablename__ = "community_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))

class Community(Base):
    __tablename__ = "community"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("community_type.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"))
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
    end: Mapped[datetime.time] = mapped_column(Time)

class Event(Base):
    __tablename__="event"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(15))
    frequency_id: Mapped[str] = mapped_column(ForeignKey("event_detail.id"))
    time_id: Mapped[int] = mapped_column(ForeignKey("time.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    weekday_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    discipline_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    auditorium_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))

Base.metadata.create_all(sync_engine)