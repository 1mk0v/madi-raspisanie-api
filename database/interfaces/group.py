from . import Interface
from MADI.models import Group
from database.schemas import group


class GroupsDB(Interface):
    pass

DBGroups = GroupsDB(
    model=Group,
    schema=group
    )


