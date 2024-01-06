from database.interfaces.schedule import ScheduleDatabaseInterface
from models import Response, LessonInfo
from fastapi import APIRouter, HTTPException, Depends
from requests import exceptions as requests_exc
from bridges.institutes_requests import madi as madiRequests 
from bridges import madi, Generator
import dependencies
import exceptions as exc


router = APIRouter(prefix='/schedule', tags=['Schedule'])
scheduleTable = ScheduleDatabaseInterface()
raspisanieTeachers = madiRequests.RaspisanieTeachers()
raspisanieGroups = madiRequests.RaspisanieGroups()
raspisanieDepartments = madiRequests.RaspisanieDepartments()


@router.get(
        "/group/{id}",
        summary = "GET group schedule",
        description="By default get actual schedule for any group, but you can get old schedule",
)
async def getGroupSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieGroups.get_schedule(id, sem, year, name)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError):
        try:
            return Response(statusCode=200, data=(await scheduleTable.getByGroupId(id)))
        except exc.BaseClientException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)

@router.get(
        "/teacher/{id}",
        summary = "GET teacher schedule",
        description="By default get actual schedule for teacher, but you can get old schedule",
)
async def getTeacherSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieTeachers.get_schedule(id, year, sem)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        try:
            return await scheduleTable.getByTeacherId(id)
        except exc.BaseClientException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)

@router.get(
        "/department/{id}",
        summary = "GET department schedule",
        description="By default get actual schedule for department, but you can get old schedule",
)
async def getDepartmentSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanieDepartments.get_schedule(id, sem, year)
        generator = Generator(bridge=madi.MADIBridge(html))
        return await generator.generateSchedule()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        try:
            return await scheduleTable.getByColumn(columnName='department_id', columnValue=id)
        except exc.BaseClientException as error:
            raise HTTPException(status_code=error.status_code, detail=error.detail)
        
@router.post(
        "/add",
        summary = "ADD schedule",
        description="",
)
async def addSchedule(schedule:LessonInfo):
    try:
        return await scheduleTable.add(schedule)
    except exc.BaseClientException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

@router.delete('/{id}/delete')
async def delSchedule(id:int):
    return await scheduleTable.delete(id=id)