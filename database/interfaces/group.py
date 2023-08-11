from . import Main
from MADI.models import Group
from database.schemas import group


class GroupsDB(Main):
    pass

DB_Groups = GroupsDB(
    model=Group,
    schema=group
    )


