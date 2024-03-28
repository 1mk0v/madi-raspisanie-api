from bridges.institutes_requests import madi as madiRequirements
from bridges.institutes_requests import BaseRequests
from sqlalchemy import select
from database import schemas, database
from events import EventsTableInterface
from models import AuditoriumInfo, Time, Community
from typing import List, Dict
from utils import removeDuplicateSpaces
import re
class AuditoriumsRaspisanie:

    def __init__(self) -> None:
        self.madi_contacts_api = BaseRequests('https://www.madi.ru/phone/phone/')
        self.raspisanieDepartments = madiRequirements.RaspisanieDepartments()
        self.auditorium_regular = r'\d{3}\w{0,2}'
        self.time_regular = r'\d\d\:\d\d \- \d\d\:\d\d'

    async def get_reserved(self):
        """
        Long response time ~1.3sec
        """
        res = self.madi_contacts_api._get(headers={"x-requested-with": "XMLHttpRequest"}).json()
        data = list()
        for item in res['aaData']:
            for auditorium in re.findall(self.auditorium_regular, item[5]):
                if auditorium not in data: data.append(auditorium)
        return data

    async def get_all(self, department_id, sem, year):
        res = await self.raspisanieDepartments.get_auditoriums(department_id, sem, year)
        res = res.find_all('tr')
        weekday:str
        data:Dict[str, List[AuditoriumInfo]] = dict()
        for item in res:
            auditorium = re.search(self.auditorium_regular, item.text)
            time = re.search(self.time_regular, item.text)
            if auditorium and time:
                lesson = item.find_all('td')
                times = time[0].split(' - ')
                frequency = lesson[1].text
                teacher = removeDuplicateSpaces(lesson[5].text)
                if auditorium[0] not in data: data[auditorium[0]] = list()
                data[auditorium[0]].append(
                    AuditoriumInfo(
                        time=Time(
                            start=times[0],
                            end=times[1]
                        ),
                        frequency=frequency,
                        weekday=weekday,
                        who_occupied=Community(
                            value=teacher,
                            department_id=department_id
                        )
                    )
                )
            else:
                tmp_weekday = item.find('th')
                if tmp_weekday: weekday = tmp_weekday.text
        return data
    
class AuditoriumsDB(database.DatabaseInterface):
    
    def __init__(
            self,
            table: database.DeclarativeAttributeIntercept | schemas.Base = schemas.Auditorium,
            engine: database.AsyncEngine = database.async_engine
        ) -> None:
        self.events = EventsTableInterface(engine=engine)
        super().__init__(table, engine)

    async def get_by_department(self, dep_id):

        base_query = select(self.table.id).where(self.table.department_id == dep_id)
        query = self.events.base_query.where(self.events.table.auditorium_id == base_query.c['id'])
        print(query)
        return await self._execute_query(query)
