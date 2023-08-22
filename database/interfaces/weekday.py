from . import Interface
from MADI.models import Essence as Weekday
from database.schemas import weekday


class WeekdayDB(Interface):
    pass

DBWeekday = WeekdayDB(
    model=Weekday,
    schema=weekday
)