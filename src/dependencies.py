from utils import get_current_sem, get_current_year, get_current_day, get_current_exam_sem
from fastapi import Query
from typing import Annotated

def current_year(year:Annotated[int, Query(ge = 19, le = get_current_year()+1)] = get_current_year()):
    return year

def current_sem(sem: Annotated[int, Query(ge = 1, le = 2)] = get_current_sem()):
    return sem

def current_exam_sem(sem: Annotated[int, Query(ge = 1, le = 2)] = get_current_exam_sem()):
    return sem

def current_day(day: Annotated[int, int] = get_current_day()):
    return day

