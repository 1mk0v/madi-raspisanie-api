from typing import List
from madi import RaspisanieTeachers
from utils import get_current_sem, get_current_year, remove_garbage
from .schemas import Teacher

raspisanie_teachers = RaspisanieTeachers()

async def find_by_names(teachers:List, dep_id:int = None) -> List[Teacher]:
    res = list()
    html = await raspisanie_teachers.get(
        sem=get_current_sem(),
        year=get_current_year()
    )
    all_teachers = [element.text for element in html]
    for teacher in teachers:
        res.append(
            Teacher(
                id = html[all_teachers.index(teacher)]['value'],
                value = remove_garbage(teacher),
                department_id=dep_id)
        )
    return res

