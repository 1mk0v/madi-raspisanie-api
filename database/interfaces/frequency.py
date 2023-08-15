from . import Interface
from MADI.models import Essence as Frequency
from database.schemas import frequency


class FrequencyDB(Interface):
    pass

DBFrequency = FrequencyDB(
    model=Frequency,
    schema=frequency
)