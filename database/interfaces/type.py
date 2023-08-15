from . import Interface
from MADI.models import Essence as Type
from database.schemas import type


class TypeDB(Interface):
    pass

DBType = TypeDB(
    model=Type,
    schema=type
)