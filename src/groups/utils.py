from typing import List
from madi import RaspisanieGroups
from utils import get_current_sem, get_current_year, remove_garbage
from .schemas import Group

raspisanie_teachers = RaspisanieGroups()

async def find_by_names(groups:List, dep_id:int = None) -> List[Group]:
    """_summary_

    Args:
        groups (List): NONE SORTED!
        dep_id (int, optional): _description_. Defaults to None.

    Returns:
        _type_: List[Teacher]
    """
    res = list()
    html = await raspisanie_teachers.get()
    all_groups = [element.text for element in html]
    for group in groups:
        if group:
            res.append(
                Group(
                    id = html[all_groups.index(group)]['value'],
                    value = remove_garbage(group),
                    department_id=dep_id)
            )
    return res