from bs4 import BeautifulSoup as bs
from models import Time, Community, LessonInfo, Schedule, Essence
from bridges import Bridge
from typing import Any, List
from utils import removeDuplicateSpaces

class Formater():

    class Schedule():

        def __init__(self) -> None:
            self.weekday = None
            self.__schedule = None
            self.teacher = None
            self.weekdays = ['Понедельник','Вторник','Среда','Четверг','Пятница', 'Суббота', 'Воскресенье']

        @property
        def schedule(self):
            return self.__schedule
        
        def setScheduleGroup(self, value:List[str]):
            if len(value) > 3:
                time = value[0].split(' - ')
                self.__schedule = LessonInfo(
                    friequency=value[3], 
                    time=Time(start=time[0], end=time[1]),
                    discipline=value[1],
                    type=value[2],
                    auditorium=value[4],
                    teacher=Community(value = removeDuplicateSpaces(value[5])),
                    weekday=self.weekday
                )
            else:
                self.__schedule = LessonInfo(
                    weekday=value[0],
                    type=value[1],
                    friequency=value[2],
                    discipline=self.weekday
                )

        def setScheduleTeacher(self, value:List[str]):
            time = value[0].split(' - ')
            self.__schedule = LessonInfo(
                    friequency=value[4],
                    time=Time(start=time[0], end=time[1]),
                    discipline=value[2],
                    type=value[3],
                    auditorium=value[5],
                    group=Community(value = value[1]),
                    weekday=self.weekday
                )

        def setScheduleDepartment(self, value:List[str]):
            time = value[0].split(' - ') 
            self.__schedule = LessonInfo(
                    friequency=value[1],
                    time=Time(start=time[0], end=time[1]),
                    discipline=value[4],
                    type=value[5],
                    auditorium=value[2],
                    group=Community(value = value[3]),
                    teacher=Community(value = self.teacher),
                    weekday=self.weekday
                )
            
        def fromGroupToLesson(self, list) -> LessonInfo:
            if len(list) == 1:
                self.weekday = list[0]
                self.__schedule = None
            else:
                self.setScheduleGroup(list)
            return self.schedule
                
        def fromTeacherToLesson(self, list) -> LessonInfo:
            if len(list) == 1:
                self.weekday = list[0]
                self.__schedule = None
            else:
                self.setScheduleTeacher(list)
            return self.schedule

        def fromDepartmentToLesson(self, list) -> LessonInfo:
            if len(list) == 1:
                self.weekday = list[0] if list[0] in self.weekdays else self.weekday
                self.teacher = removeDuplicateSpaces(list[0]) if list[0] not in self.weekdays else self.teacher
                self.__schedule = None
            else:
                self.setScheduleDepartment(list)
            return self.schedule

    class Examination():
        def __init__(self) -> None:
            self.__schedule = None

        @property
        def schedule(self):
            return self.__schedule
        
        def setExamGroup(self, value:List[str]):
            time = value[1].split(' ')
            self.__schedule = Schedule(
                    day=time[0], 
                    time=Time(start=time[1],end=None),
                    discipline=value[0],
                    type='Экзамен',
                    auditorium=value[2],
                    teacher=Community(value = removeDuplicateSpaces(value[3]))
                )
            
        def setExamTeacher(self, value:List[str]):
            time = value[1].split(' ')
            self.__schedule = Schedule(
                    day=time[0],
                    time=Time(start=time[1],end=None),
                    discipline=value[3],
                    type='Экзамен',
                    auditorium=value[2],
                    group=Community(value =value[0])
                )
        
        def fromGroupToLesson(self, list) -> Schedule:
            self.setExamGroup(list)
            return self.schedule

        def fromTeacherToLesson(self, list) -> Schedule:
            self.setExamTeacher(list)
            return self.schedule


    def getMethod(self, title) -> Any:
        if title[0] == 'Время занятий' and title[1] == 'Наименование дисциплины':
            formater = Formater.Schedule()
            return formater.fromGroupToLesson
        if title[0] == 'Время занятий' and title[1] == 'Группа':
            formater = Formater.Schedule()
            return formater.fromTeacherToLesson
        if title[0] == 'Время' and title[1] == 'Занятия на неделе':
            formater = Formater.Schedule()
            return formater.fromDepartmentToLesson
        if title[0] == 'Наименование дисциплины' and title[1] == 'Дата и время начала экзамена':
            formater = Formater.Examination()
            return formater.fromGroupToLesson
        if title[0] == 'Группа' and title[1] == 'Дата и время начала экзамена':
            return Formater.Examination().fromTeacherToLesson


class MADIBridge(Bridge):

    def __init__(self,
                 response
                ) -> None:
        super().__init__()
        self.response:bs = response
        self.__title = None

    def _deleteFirstAndLastEmptyElements(self, array:list):
        if array[0] == '' and array[len(array)-1] == '':
            array.pop(0)
            array.pop(len(array) - 1)
        return array

    @property
    def title(self):
        if self.__title == None:
            tr:bs = self.response.find_all('tr')
            for element in tr:
                element = self._deleteFirstAndLastEmptyElements(element.get_text().split('\n'))
                if 'Аудитория' in element:
                    self.__title = element
                    break
        return self.__title

    def generateLessons(self):
        tr:bs = self.response.find_all('tr')
        method = Formater().getMethod(self.title)
        for element in tr:
            element = self._deleteFirstAndLastEmptyElements(element.get_text().split('\n'))
            if 'Аудитория' not in element:
                yield method(element)

    def generateAcademicCommunity(self):
        for element in self.response:
            if int(element['value']) > -1 and '20' not in element.text:
                yield Essence(id=element['value'], value=removeDuplicateSpaces(element.text))