from models import LessonInfo, ResponseWithLessonInfo, Time, Community
from fastapi import APIRouter, HTTPException, Depends
from requests import exceptions as requests_exc
from bridges.institutes_requests import madi as madiRequests 
from bridges import madi, Generator
from . import EventsTableInterface
import dependencies
import exceptions as exc


router = APIRouter(prefix='/event', tags=['Event'])
raspisanieTeachers = madiRequests.RaspisanieTeachers()
raspisanieGroups = madiRequests.RaspisanieGroups()
raspisanieDepartments = madiRequests.RaspisanieDepartments()


@router.get(
        "/",
        summary = "GET group schedule",
        description="By default get actual schedule for any group, but you can get old schedule",
        deprecated=True
)
async def getGroupSchedule():
    try:
        event_table = EventsTableInterface()
        res = (await event_table.get_by_group_id(1)).all()
        table = list()
        print(res)
        for item in res:
            data = item._mapping
            print(data)
            time = Time.model_validate(data)
            lesson_info = LessonInfo.model_validate(data)
            lesson_info.time = time
            table.append(lesson_info)
        return table
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])

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
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])

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
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])
    

@router.get(
        "/lessons/department/{id}",
        summary = "GET department schedule",
        description="By default get actual schedule for department, but you can get old schedule",
        response_model=ResponseWithLessonInfo
)
async def getDepartmentSchedule(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieDepartments.get_schedule(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError)  as error:
        raise HTTPException(status_code=500, detail=error.args[0])
    

@router.get("/exam/group/{id}",
        summary = "GET group exams",
        description="By default get actual exams for any group, but you can get old exams",
        response_model=ResponseWithLessonInfo
)
async def getGroupExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieGroups.get_schedule(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])


@router.get(
        "/exam/teacher/{id}",
        summary = "GET teacher exam",
        description="By default get actual exam for teacher, but you can get old exam",
        response_model=ResponseWithLessonInfo
)
async def getTeacherExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieTeachers.get_schedule(id, year, sem)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        raise HTTPException(status_code=500, detail=error.args[0])
    

@router.get(
        "/exam/department/{id}",
        summary = "GET department exam",
        description="By default get actual exam for department, but you can get old exam",
        response_model=ResponseWithLessonInfo
)
async def getDepartmentExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieDepartments.get_schedule(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError)  as error:
        raise HTTPException(status_code=500, detail=error.args[0])
    

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
    

@router.get(
        "/custom/department/{id}",
        summary = "GET department events by custom event type",
        response_model=ResponseWithLessonInfo
)
async def getDepartmentExam(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    pass