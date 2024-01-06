from database.interfaces.schedule import ExaminationDatabaseInterface
from database.schemas import exam
from models import Response, Schedule
from fastapi import APIRouter, HTTPException, Depends
import dependencies
from bridges import madi, Generator
from bridges.institutes_requests import madi as madiRequests
from requests import exceptions as requests_exc
import exceptions as exc

router = APIRouter(prefix='/exam', tags=['Exam'])
examTable = ExaminationDatabaseInterface(schema=exam)
raspisanieGroups = madiRequests.RaspisanieGroups()
raspisanieTeachers = madiRequests.RaspisanieTeachers()


@router.get(
        "/group/{id}",
        summary = "GET group exams",
        description="By default get actual schedule for any group, but you can get old schedule",
)
async def getGroupExam(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieGroups.get_exam(id,sem,year,name)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode = 200, data=await examTable.getByGroupId(id))
        except exc.NotFoundError as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
    

@router.get(
        "/teacher/{id}",
        summary = "GET teacher exams",
        description="By default get actual schedule for teacher, but you can get old schedule",
)
async def getTeacherExam(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieTeachers.get_exam(id, year, sem)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode = 200, data = await examTable.getByTeacherId(id))
        except exc.BaseClientException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)

@router.post("/add")
async def add(exam:Schedule):
    try:
        return Response(statusCode=201, data=await examTable.add(exam))
    except exc.BaseClientException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.delete('/{id}/delete')
async def delExam(id:int):
    return await examTable.delete(id)


