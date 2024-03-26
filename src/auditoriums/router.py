from fastapi import APIRouter
from bridges.institutes_requests import madi as madiRequirements
from . import Auditoriums

router = APIRouter(prefix='/auditoriums', tags=['Auditoriums'], deprecated=True)
raspisanieDepartments = madiRequirements.RaspisanieDepartments()

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