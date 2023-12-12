from madi import RaspisanieDepartments
from database.interfaces import Interface 
from database.schemas import auditorium
from models import Essence as AuditoriumModel

class Auditoriums:

    def __init__(self) -> None:
        self.auditorium = Interface(AuditoriumModel, auditorium)
        self.raspisanieDepartments = RaspisanieDepartments()

    def getAllFreeAuditoriums(self):
        return self.raspisanieDepartments.get()
