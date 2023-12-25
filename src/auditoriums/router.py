from fastapi import APIRouter, HTTPException, Depends
from database.interfaces import Interface
from madi import RaspisanieDepartments
from models import Community
from database.schemas import auditorium
from bridges import madi
from requests import exceptions
import datetime
import dependencies
from schedule import router as scheduleRouter
from models import LessonInfo, List

router = APIRouter(prefix='/auditoriums', tags=['Auditoriums'])
raspisanieDepartments = RaspisanieDepartments()
auditoriumsTable = Interface(schema=auditorium, model=Community)

@router.get(
        "/department/{id}",
        summary = "GET department auditoriums",
        # description="By default get actual schedule for teacher, but you can get old schedule",
)
async def getDepartmentAuditoriums(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):  
    auditoriums = list()
    try:
        html = await raspisanieDepartments.get_auditoriums(id, sem, year)
        bridge = madi.MADIBridge(html)
        for i in bridge.generateLessons():
            if i != None and i.auditorium not in auditoriums: auditoriums.append(i.auditorium)
        return auditoriums
    except (exceptions.ConnectionError, ValueError) as error:
        raise HTTPException(404, detail=error.args[0])
    

@router.get(
        "/department/{id}/free",
        summary = "GET free departments auditoriums" 
)
async def getFreeDepartmentAuditoriums(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    currentDatetime = datetime.datetime.now()
    try:
        busyAuditoriums = list()
        freeAuditoriums = list()
        schedules:List[LessonInfo] = (await scheduleRouter.getDepartmentSchedule(id, sem=sem, year=year)).data
        for schedule in schedules:
            if currentDatetime.time() > schedule.date.time.start \
            and currentDatetime.time() < schedule.date.time.end:
                if schedule.auditorium not in busyAuditoriums: busyAuditoriums.append(schedule.auditorium)
                if schedule.auditorium in freeAuditoriums: freeAuditoriums.remove(schedule.auditorium)
            if schedule.auditorium not in busyAuditoriums \
                and currentDatetime.time() < schedule.date.time.start:
                if datetime.datetime.combine(currentDatetime.now(), schedule.date.time.start) - currentDatetime > datetime.timedelta(minutes=30):
                    freeAuditoriums.append(schedule.auditorium)
        return freeAuditoriums
    except Exception as error:
        print(error)


@router.post(
    "/add",
    summary = "POST auditorium"
)
async def addAuditorium(
    value:str
):
    try:
        return await auditoriumsTable.add(value)
    except Exception as error:
        raise HTTPException(500, detail=error.args[0])
    