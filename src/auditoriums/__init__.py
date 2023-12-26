from madi import RaspisanieDepartments
from database.interfaces import Interface 
from database.schemas import auditorium
from models import Community as AuditoriumModel, LessonInfo, List
from schedule import router as scheduleRouter
import datetime
import utils
class Auditoriums:

    def __init__(self, dep_id = 61) -> None:
        self.auditorium = Interface(AuditoriumModel, auditorium)
        self.raspisanieDepartments = RaspisanieDepartments()
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
    
    async def getBusyAuditoriums(self):
        busyAuditoriums = list()
        currentDatetime = datetime.datetime.now()
        schedules:List[LessonInfo] = (await scheduleRouter.getDepartmentSchedule(id = self.departmentId)).data
        for schedule in schedules:
            if schedule.weekday == self.days[currentDatetime.today().weekday()] \
            and schedule.date.friequency in self.weekdayTypes[currentDatetime.isocalendar().week%2]:
                if currentDatetime.time() > schedule.date.time.start \
                and currentDatetime.time() < schedule.date.time.end:
                    busyAuditoriums.append(schedule)
        return busyAuditoriums
    
    async def getFreeAuditoriums(self):
        currentDatetime = datetime.datetime.now()
        schedules:List[LessonInfo] = (await scheduleRouter.getDepartmentSchedule(id = self.departmentId,
                                                                                 sem=utils.get_current_sem(),
                                                                                 year=utils.get_current_year())).data
        for schedule in schedules:
            if schedule.weekday == self.days[currentDatetime.today().weekday()] \
            and schedule.date.friequency in self.weekdayTypes[currentDatetime.isocalendar().week%2]:
                if currentDatetime.time() > schedule.date.time.end:
                    print(currentDatetime.time(), schedule, '\n')
