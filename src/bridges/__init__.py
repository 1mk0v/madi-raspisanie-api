"""
    Модуль позволяет переводить в читабельный для программы формат расписания
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator
from models import Response

class Bridge(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def generateLessons(self) -> AsyncGenerator:
        pass

    @abstractmethod
    async def generateAcademicCommunity(self) -> AsyncGenerator:
        pass


class Generator():
    
    def __init__(self,
                 bridge:Bridge
                ) -> None:
        self.bridge = bridge
        self.__community = Response(statusCode=200, data=list())
        self.__schedule = Response(statusCode=200, data=list())

    async def generateSchedule(self):
        if len(self.__schedule.data) == 0:
            await self.__generateSchedule()
        return self.__schedule

    async def __generateSchedule(self):
        for lesson in self.bridge.generateLessons():
            if lesson != None:
                self.__schedule.data.append(lesson)

    async def generateListOfCommunity(self):
        if len(self.__community.data) == 0:
            await self.__generateListOfCommunity()
        return self.__community

    async def __generateListOfCommunity(self):
        for community in self.bridge.generateAcademicCommunity():
            if community != None:
                self.__community.data.append(community)