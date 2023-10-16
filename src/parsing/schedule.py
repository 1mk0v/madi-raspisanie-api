from models import Response
from bridges import Bridge

class Schedule():
    
    def __init__(self,
                 bridge:Bridge
                ) -> None:
        self.bridge = bridge
        self.__schedule = Response(statusCode=200, data=list())

    @property
    async def schedule(self):
        if len(self.__schedule.data) == 0:
            await self.__generateSchedule()
        return self.__schedule

    async def __generateSchedule(self):
        for lesson in self.bridge.generateLessons():
            if lesson != None:
                self.__schedule.data.append(lesson) 
