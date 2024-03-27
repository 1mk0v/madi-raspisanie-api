from models import ResponseWithLessonInfo, Response
from fastapi import APIRouter, HTTPException, Depends
from requests import exceptions as requests_exc
from bridges.institutes_requests import madi as madiRequests 
from bridges import madi, Generator
from . import EventsTableInterface
from .utils import get_validate_event
import dependencies
import exceptions as exc


router = APIRouter(prefix='/event', tags=['Event'])
raspisanieTeachers = madiRequests.RaspisanieTeachers()
raspisanieGroups = madiRequests.RaspisanieGroups()
raspisanieDepartments = madiRequests.RaspisanieDepartments()


@router.get(
    "/lessons/group/{id}",
    summary = "GET group schedule",
    description="By default get actual schedule for any group, but you can get old schedule",
    response_model=ResponseWithLessonInfo
)
async def getGroupSchedule(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieGroups.get_schedule(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        event_table = EventsTableInterface()
        res = (await event_table.get_lessons_by_group_id(id)).all()
        return Response(data=get_validate_event(res))


@router.get(
    "/lessons/teacher/{id}",
    summary = "GET teacher schedule",
    description="By default get actual schedule for teacher, but you can get old schedule",
    response_model=ResponseWithLessonInfo
)
async def getTeacherSchedule(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieTeachers.get_schedule(id, year, sem)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        event_table = EventsTableInterface()
        res = (await event_table.get_lessons_by_teacher_id(id)).all()
        return Response(data=get_validate_event(res))


@router.get("/exam/group/{id}",
    summary = "GET group exams",
    description="By default get actual exams for any group, but you can get old exams",
    response_model=ResponseWithLessonInfo
)
async def getGroupExam(
    id:int,
    sem = Depends(dependencies.current_exam_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieGroups.get_exam(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        event_table = EventsTableInterface()
        res = (await event_table.get_exam_by_group_id(id)).all()
        return Response(data=get_validate_event(res))


@router.get(
    "/exam/teacher/{id}",
    summary = "GET teacher exam",
    description="By default get actual exam for teacher, but you can get old exam",
    response_model=ResponseWithLessonInfo
)
async def getTeacherExam(
    id:int,
    sem = Depends(dependencies.current_exam_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieTeachers.get_exam(id, year, sem)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        event_table = EventsTableInterface()
        res = (await event_table.get_exam_by_teacher_id(id)).all()
        return Response(data=get_validate_event(res))


@router.get(
    "/custom/group/{id}",
    summary = "GET groups events by custom event type",
    response_model=ResponseWithLessonInfo
)
async def getGroupExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    pass


@router.get(
    "/custom/teacher/{id}",
    summary = "GET teachers events by custom event type",
    response_model=ResponseWithLessonInfo
)
async def getTeacherExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    pass