from database.interfaces.exam import ExamDatabaseInterface
from models import Response, Schedule
from requests import exceptions
from fastapi import APIRouter, HTTPException, Depends, status
import dependencies
from bridges import madi, Generator
import madi as madiRequests


router = APIRouter(prefix='/exam', tags=['Exam'])
examTable = ExamDatabaseInterface()
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
    except (exceptions.ConnectionError, ValueError):
        try:
            return examTable.getByGroupId(id)
        except ValueError:
            raise HTTPException(404)
    

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
    except (exceptions.ConnectionError, ValueError) as error:
        try:
            return await examTable.getByTeacherId(id)
        except ValueError as error:
            raise HTTPException(404)


@router.post("/add")
async def add(exam:Schedule):
    try:
        await examTable.add(exam)
        return Response(statusCode=201, data=exam)
    except Exception as error:
        raise HTTPException(500, detail=error.args[0])


@router.delete('/{id}/delete')
async def delExam(id:int):
    return await examTable.delete(id)


