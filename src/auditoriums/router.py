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
        "/department/{id}/busy",
        summary = "GET free departments auditoriums" 
)
async def getFreeDepartmentAuditoriums(
    id:int,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year),
):
    days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    weekdayType = {
        1: ['Числитель', 'Числ. 1 раз в месяц', 'Еженедельно'],
        0: ['Знаменатель', 'Знам. 1 раз в месяц', 'Еженедельно']
    }
    currentDatetime = datetime.datetime.now()
    busyAuditoriums = list()
    try:
        schedules:List[LessonInfo] = (await scheduleRouter.getDepartmentSchedule(id, sem=sem, year=year)).data
        for schedule in schedules:
            if schedule.weekday == days[currentDatetime.today().weekday()] \
            and schedule.date.friequency in weekdayType[currentDatetime.isocalendar().week%2]:
                if currentDatetime.time() > schedule.date.time.start \
                and currentDatetime.time() < schedule.date.time.end:
                    busyAuditoriums.append(schedule.auditorium)
        return busyAuditoriums
    except Exception as error:
        print(error, 'error')


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
    