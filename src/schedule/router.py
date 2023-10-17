from database.interfaces.schedule import ScheduleDatabaseInterface
from models import Response, LessonInfo
from fastapi import APIRouter, HTTPException, Depends
from requests import exceptions
import dependencies
import madi as madiRequests
from bridges import madi, Generator

router = APIRouter(prefix='/schedule', tags=['Schedule'])
scheduleTable = ScheduleDatabaseInterface()
raspisanieTeachers = madiRequests.RaspisanieTeachers()
raspisanieGroups = madiRequests.RaspisanieGroups()


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
        return Response(statusCode=200, data=await generator.generateSchedule())
    except (exceptions.ConnectionError, ValueError):
        try:
            return Response(statusCode=200, data=await scheduleTable.getByGroupId(id))
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])


#---------------Teacher---------------#

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
        return Response(statusCode=200, data=await generator.generateSchedule())
    except (exceptions.ConnectionError, ValueError) as error:
        try:
            return scheduleTable.getByTeacherId(id)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])

@router.post(
        "/add",
        summary = "ADD schedule",
        description="",
)
async def addSchedule(schedule:LessonInfo):
    return await scheduleTable.add(schedule)

@router.delete('/{id}/delete')
async def delSchedule(id:int):
    return await scheduleTable.delete(id=id)