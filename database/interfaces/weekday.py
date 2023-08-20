from . import Interface
from MADI.models import Essence as Weekday
from database.schemas import week_day


class WeekdayDB(Interface):
    pass

DBWeekday = WeekdayDB(
    model=Weekday,
    schema=week_day
)