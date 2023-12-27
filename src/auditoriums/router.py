from fastapi import APIRouter
from database.interfaces import Interface
from madi import RaspisanieDepartments
from models import Community
from database.schemas import auditorium
from . import Auditoriums

router = APIRouter(prefix='/auditoriums', tags=['ASU Auditoriums'])
raspisanieDepartments = RaspisanieDepartments()
auditoriumsTable = Interface(schema=auditorium, model=Community)

@router.get(
        "/asu",
        summary = "GET department auditoriums",
)
async def getDepartmentAuditoriums():
    auditorium = Auditoriums()
    return await auditorium.getAllAuditoriums()


@router.get(
        "/asu/free",
        summary = "GET free departments auditoriums" 
)
async def getFreeDepartmentAuditoriums():
    auditorium = Auditoriums()
    return await auditorium.getFreeAuditoriums()


@router.get(
        "/asu/schedule",
        summary = "GET free departments auditoriums" 
)
async def getSchedule():
    auditorium = Auditoriums()
    return (await auditorium._getBusyAuditoriums())[0]