from fastapi import APIRouter
from database.interfaces import Interface
from bridges.requests import madi as madiRequirements
from models import Community
from database.schemas import auditorium
from . import Auditoriums

router = APIRouter(prefix='/auditoriums', tags=['ASU Auditoriums'])
raspisanieDepartments = madiRequirements.RaspisanieDepartments()
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
        summary = "GET free departments auditoriums",
        deprecated=True
)
async def getFreeDepartmentAuditoriums():
    auditorium = Auditoriums()
    return await auditorium.getFreeAuditoriums()


@router.get(
        "/asu/busy",
        summary = "GET free departments auditoriums",
        deprecated=True
)
async def getSchedule():
    auditorium = Auditoriums()
    return (await auditorium._getBusyAuditoriums())[0]