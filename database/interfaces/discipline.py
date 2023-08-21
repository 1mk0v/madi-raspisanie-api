from . import Interface
from MADI.models import Essence as Discipline
from database.schemas import discipline


class DisciplineDB(Interface):
    pass

DBDiscipline = DisciplineDB(
    model=Discipline,
    schema=discipline
)