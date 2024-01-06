from fastapi import APIRouter, HTTPException, Depends
from database.interfaces.academic_community import AcademicCommunityDatabaseInterface
from bridges.institutes_requests import madi as madiRequests
from models import Response, Community
from database.schemas import teacher
from bridges import madi, Generator
from requests import exceptions as requests_exc
import exceptions as exc
import dependencies

router = APIRouter(prefix='/teacher', tags=['Teachers'])
raspisanie_teachers = madiRequests.RaspisanieTeachers()
teacherTable = AcademicCommunityDatabaseInterface(schema=teacher)

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
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode=200, data=(await teacherTable.getActual()))
        except exc.BaseClientException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
    

@router.post('/add')
async def add_teacher(
    teacher:Community
):
    try:
        return Response(statusCode=201, data=(await teacherTable.add(teacher)))
    except exc.BaseAppException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    

@router.delete('/{id}/delete')
async def delete_teacher(
    id:int
):
    return await teacherTable.delete(id)
