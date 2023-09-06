from models import Essence, Time
from typing import List

class Department(Essence):
    pass

class Auditorium(Essence):
    busy:List[Time] | None = None