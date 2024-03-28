from fastapi import APIRouter, Depends, HTTPException
from bridges.institutes_requests import madi as madiRequirements
from exceptions import BaseAppException
from dependencies import current_sem, current_year
from models import AuditoriumInfo
from . import AuditoriumsRaspisanie, AuditoriumsDB
from .utils import get_validate_auditoriums
from typing import List, Dict, AnyStr

router = APIRouter(prefix='/auditoriums', tags=['Auditoriums'])
raspisanieDepartments = madiRequirements.RaspisanieDepartments()

@router.get(
        '/reserved',
        summary="GET reserved auditoriums",
        description="Long response time (~1.3sec). Be careful to use this handler.",
        response_model=List[str]
)
async def get_reserved_auditoriums():
    try:
        auditoriums = AuditoriumsRaspisanie()
        return await auditoriums.get_reserved()
    except BaseAppException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get(
        "/all/{dep_id}",
        summary = "GET department auditoriums"
        # response_model=Dict[AnyStr, List[AuditoriumInfo]]
)
async def getDepartmentAuditoriums(dep_id:int, sem:int = Depends(current_sem), year:int = Depends(current_year)):
    try:
        # raise BaseAppException(status_code=400)
        auditoriums = AuditoriumsDB()
        res = await auditoriums.get_by_department(dep_id)
        return get_validate_auditoriums(res.fetchall())
    except BaseAppException as error:
        auditoriums = AuditoriumsRaspisanie()
        return await auditoriums.get_all(dep_id, sem, year)
        # raise HTTPException(status_code=error.status_code, detail=error.detail)