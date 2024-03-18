from .database import sync_engine
from sqlalchemy import (
    String, Time, ForeignKey, Integer, text
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

class EventTime(Base):
    __tablename__ = "event_time"

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime.time] = mapped_column(Time) 
    end: Mapped[datetime.time] = mapped_column(Time, nullable=True)

class Event(Base):
    __tablename__="event"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(15), nullable=True)
    frequency_id: Mapped[str] = mapped_column(ForeignKey("event_detail.id"), nullable=True)
    event_time_id: Mapped[int] = mapped_column(ForeignKey("event_time.id"), nullable=True)
    # event_time: Mapped["EventTime"] = relationship("EventTime", backref='event_time')
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"), nullable=True)
    weekday_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"), nullable=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"))
    auditorium_id: Mapped[int] = mapped_column(ForeignKey("event_detail.id"), nullable=True)

Base.metadata.drop_all(sync_engine)
queries=[
    "insert into event_detail_type (value) values ('Тип недели'),('Аудитория'),('Дисциплина'),('Тип события'),('День недели');"
    ,"insert into event_detail (type_id, value) values (1, 'Числитель'), (3, 'Тестовая дисциплина'), (4, 'Лекция'), (5, 'Понедельник'), (2, '234H');"
    ,"insert into event_time (start, \"end\") values ('18:50:00', '20:20:00'), ('20:30:00', '22:00:00');"
    ,"insert into \"group\" (id, value) values (1, 'Group1'), (2, 'Group2'), (3, 'Group3');"
    ,"insert into \"teacher\" (id, value) values (1, 'Teacher1'), (2, 'Teacher2'), (3, 'Teacher3');"
    ,"insert into event (date, frequency_id, discipline_id,group_id, teacher_id, event_time_id, type_id, weekday_id, auditorium_id) values ('', 1, 2, 1, 1, 1, 3, 4, 5);"
]
Base.metadata.create_all(sync_engine)
with sync_engine.connect() as conn:
    for i in queries:
        conn.execute(text(i))
    conn.commit()