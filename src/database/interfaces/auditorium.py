from . import Interface
from models import Essence as Auditorium
from database.schemas import auditorium


class AuditoriumDB(Interface):
    pass

DBAuditorium = AuditoriumDB(
    model=Auditorium,
    schema=auditorium
)