from bridges.institutes_requests import madi as madiRequirements 
from database.interfaces import Interface 
from database.schemas import auditorium
from models import Community as AuditoriumModel, LessonInfo, List
from schedule import router as scheduleRouter
import datetime
import utils
class Auditoriums:

    def __init__(self, dep_id = 61) -> None:
        self.auditorium = Interface(AuditoriumModel, auditorium)
        self.raspisanieDepartments = madiRequirements.RaspisanieDepartments()
        self.departmentId = dep_id
        self.days = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'
        }
        self.weekdayTypes = {
            1: ['Числитель', 'Числ. 1 раз в месяц', 'Еженедельно'],
            0: ['Знаменатель', 'Знам. 1 раз в месяц', 'Еженедельно']
        }

    async def getAllAuditoriums(self):
        return await self.auditorium.getByColumn('department_id', self.departmentId)
    
    async def _getBusyAuditoriums(self):
        scheduleAuditorium = dict()
        currentDatetime = datetime.datetime.now()
        schedules:List[LessonInfo] = (await scheduleRouter.getDepartmentSchedule(
            id = self.departmentId,
            sem=utils.get_current_sem(),
            year=utils.get_current_year()
        )).data
        lessonsTime = list()
        for schedule in schedules:
            if schedule.date.time not in lessonsTime:
                lessonsTime.append(schedule.date.time)
            if schedule.weekday == self.days[currentDatetime.today().weekday()] \
            and schedule.date.friequency in self.weekdayTypes[currentDatetime.isocalendar().week%2]:
                    if schedule.auditorium not in scheduleAuditorium.keys():
                        scheduleAuditorium[schedule.auditorium] = list()
                    if schedule.date.time not in scheduleAuditorium[schedule.auditorium]:
                        scheduleAuditorium[schedule.auditorium].append(
                            schedule.date.time
                        )
        return scheduleAuditorium, sorted(lessonsTime, key = lambda x: x.start)

    async def getFreeAuditoriums(self):
        scheduleAuditorium = dict()
        allAuditoriums = await self.auditorium.getByColumn('department_id', 61)
        busyAuditoriums, scheduleTimeInfo = await self._getBusyAuditoriums()
        for auditorium in allAuditoriums:
            if auditorium['value'] not in busyAuditoriums.keys():
                scheduleAuditorium[auditorium['value']] = scheduleTimeInfo
            else:
                for time in scheduleTimeInfo:
                    if time not in busyAuditoriums[auditorium['value']]:
                        if auditorium['value'] not in scheduleAuditorium.keys(): scheduleAuditorium[auditorium['value']] = list()
                        scheduleAuditorium[auditorium['value']].append(time)
        return scheduleAuditorium