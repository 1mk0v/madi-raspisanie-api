import os
from typing import List
from madi import RaspisanieGroups
from utils import remove_garbage
from .schemas import Group

raspisanieGroups = RaspisanieGroups()


async def find_by_names(groups:List[str], dep_id:int = None) -> List[Group]:
    """
        Groups get none sorted
    """
    res = list()
    html = await raspisanieGroups.get()
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