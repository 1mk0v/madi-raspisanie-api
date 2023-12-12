from fastapi import APIRouter, HTTPException, Depends
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from madi import RaspisanieDepartments
from database.schemas import teacher
from bridges import madi, Generator
from requests import exceptions
import dependencies

router = APIRouter(prefix='/auditoriums', tags=['Auditoriums'])
raspisanieDepartments = RaspisanieDepartments()
teacherTable = AcademicCommunityDatabaseInterface(schema=teacher)

@router.get(
        "/department/{id}",
        summary = "GET department auditoriums",
        # description="By default get actual schedule for teacher, but you can get old schedule",
)
async def getDepartmentAuditoriums(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieDepartments.get_schedule(id, sem, year)
        print(html)
        return None
    except (exceptions.ConnectionError, ValueError) as error:
        raise HTTPException(404, detail=error.args[0])