from fastapi import APIRouter, HTTPException, Depends
from bridges.institutes_requests import madi as madiRequests
from models import Response, Community
# from database.schemas import teacher
from bridges import madi, Generator
from requests import exceptions as requests_exc
import exceptions as exc
import dependencies

router = APIRouter(prefix='/teacher', tags=['Teachers'])
raspisanie_teachers = madiRequests.RaspisanieTeachers()
# teacherTable = AcademicCommunityDatabaseInterface(schema=teacher)

@router.get(
    '/',
)
async def get_all_teachers(
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_teachers.get(year, sem)
        generator = Generator(madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])