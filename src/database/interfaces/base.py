from . import Interface
from models import Essence
from database import schemas

DBAuditorium = Interface(
    model = Essence,
    schema = schemas.auditorium
)

DBDepartment = Interface(
    model = Essence,
    schema = schemas.department
)

DBDiscipline = Interface(
    model = Essence,
    schema = schemas.discipline
)

DBFrequency = Interface(
    model = Essence,
    schema = schemas.frequency
)

DBType = Interface(
    model = Essence,
    schema = schemas.type
)

DBWeekday = Interface(
    model = Essence,
    schema = schemas.weekday
)