from database.interfaces.schedule import DBScheduleInfo, addToAllTableFromSchedule
from database.interfaces.group import DBGroups
from database.interfaces.base import DBDepartment
from database.models import Response_Message
from groups.schemas import Schedule as GroupSchedule, Group
from teachers.schemas import Schedule as TeacherSchedule, Teacher
from department.schemas import DepartmentSchedule 
from models import Essence as Department
from fastapi import APIRouter, HTTPException, Depends, status
from requests import exceptions
import dependencies
import madi
from .utils import parseGroupSchedule, parseTeacherSchedule, parseDepartmentSchedule
from .schemas import Schedule
from bridges.madi import MADIBridge
from parsing.schedule import Schedule as ParseSchedule
router = APIRouter(prefix='/schedule', tags=['Schedule'])
    

#---------------Group---------------#
raspisanie_groups = madi.RaspisanieGroups()

@router.get(
        "/group/{id}",
        summary = "GET group schedule",
        description="By default get actual schedule for any group, but you can get old schedule",
        responses={
            status.HTTP_200_OK:{
                "model":GroupSchedule,
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
    }
)
async def getGroupSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_groups.get_schedule(id, sem, year, name)
        bridge = MADIBridge(html)
        schedule = ParseSchedule(bridge=bridge)
        return await schedule.schedule
    except (exceptions.ConnectionError, ValueError):
        try:
            group = await DBGroups.get_by_column('id', id)
            schedule = await DBScheduleInfo.get_by_group(id)
            return GroupSchedule(group=group[0], schedule=schedule)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])


#---------------Teacher---------------#
raspisanie_teachers = madi.RaspisanieTeachers()

@router.get(
        "/teacher/{id}",
        summary = "GET teacher schedule",
        description="By default get actual schedule for teacher, but you can get old schedule",
        responses={
            status.HTTP_200_OK:{
                "model":TeacherSchedule,
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
    })
async def getTeacherSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_teachers.get_schedule(id, year, sem)
        return await parseTeacherSchedule(html=html, teacher=Teacher(id=id, value=name))
    except (exceptions.ConnectionError, ValueError) as error:
        try:
            teacher = Teacher(id=id, value=name)
            schedule = await DBScheduleInfo.get_by_teacher(id=id)
            return TeacherSchedule(teacher = teacher, schedule = schedule)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])

#---------------Department---------------#

raspisanie_departments = madi.RaspisanieDepartments()

@router.get(
        '/department/{id}',
        summary = "GET department schedule",
)
async def getDepartmentSchedule(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_departments.get_schedule(id, sem, year)
        return await parseDepartmentSchedule(html, Department(id=id,value=name))
    except (exceptions.ConnectionError, ValueError) as error:
        try:
            raise ValueError("Can't find schedule")
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])


@router.post(
        '/add/department/{id}',
        summary = "ADD schedule by department",
)
async def addDepartmentSchedule(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    response = list()
    score:int = 0
    scheduleData:DepartmentSchedule = await getDepartmentSchedule(id=id, sem=sem, year=year)
    schedule = scheduleData.schedule
    for key in schedule:
        for lesson in schedule[key]:
            data = Schedule(date=lesson.date, discipline=lesson.discipline,
                            type=lesson.type, auditorium=lesson.auditorium, weekday=key,
                            group=lesson.group, teacher=lesson.teacher)
            scheduleData = await addToAllTableFromSchedule(data)
            id = await DBScheduleInfo.add(scheduleData)
            response.append(Response_Message(id=id))
            score +=1
    print(score)
    return response


#---------------Schedule------ ---------#

@router.post("/add")
async def addSchedule(schedule:Schedule):
    schedule_data = await addToAllTableFromSchedule(schedule)
    id = await DBScheduleInfo.add(schedule_data)
    return Response_Message(id=id)


@router.delete('/{id}/delete')
async def delSchedule(id:int):
    return await DBScheduleInfo.delete(id=id)