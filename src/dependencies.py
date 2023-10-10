from utils import get_current_sem, get_current_year
from fastapi import Query
from typing import Annotated

def current_year(year:Annotated[int, Query(ge = 19, le = get_current_year()+1)] = get_current_year()):
    return year

def current_sem(sem: Annotated[int, Query(ge = 1, le = 2)] = get_current_sem()):
    return sem