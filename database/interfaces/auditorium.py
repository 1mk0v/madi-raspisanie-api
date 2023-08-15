from . import Interface
from MADI.models import Essence as Auditorium
from database.schemas import teacher


class AuditoriumDB(Interface):
    pass

DB = AuditoriumDB(
    model=Auditorium,
    schema=teacher
)