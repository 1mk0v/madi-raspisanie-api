from bs4 import BeautifulSoup as bs
from models import Date, Time, Group, Teacher
from bridges import Bridge, LessonInfo
from typing import List
from utils import remove_spaces

class Formater():

    def __init__(self) -> None:
        pass

    class Schedule():

        def __init__(self) -> None:
            self.weekday = None
            self.__schedule = None

        @property
        def schedule(self):
            return self.__schedule
        
        def __setScheduleGroup(self, value:List[str]):
            if len(value) > 3:
                time = value[0].split(' - ')
                date = Date(friequency=value[3], time=Time(start=time[0], end=time[1])) 
                self.__schedule = LessonInfo(
                    date=date,
                    discipline=value[1],
                    type=value[2],
                    auditorium=value[4],
                    teacher=Teacher(value = remove_spaces(value[5])),
                    weekday=self.weekday
                )
            else:
                self.__schedule = LessonInfo(
                    weekday=value[0],
                    type=value[1], 
                    date=Date(friequency=value[2]),
                    discipline=self.weekday
                )

        def __setScheduleTeacher(self, value:List[str]):
            pass

        def __setScheduleDepartment(self, value:List[str]):
            pass

        def fromGroupToLesson(self, list):
            if len(list) == 1:
                self.weekday = list[0]
                self.__schedule = None
            else:
                self.__setScheduleGroup(list)
            return self.schedule
                
        def fromTeacherToLesson(self, list) -> LessonInfo:
            print('SCHEDULE','TEACHER',list)
            pass

        def fromDepartmentToLesson(self, list) -> LessonInfo:
            print('SCHEDULE','DEPARTMENT',list)
            pass

    class Examination():

        def fromGroupToLesson(self, list) -> LessonInfo:
            pass

        def fromTeacherToLesson(self, list) -> LessonInfo:
            pass
    
    def getMethod(self, title) -> LessonInfo:
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
            formater = Formater.Examination()
            return formater.fromTeacherToLesson



class MADIBridge(Bridge):

    def __init__(self,
                 response
                ) -> None:
        super().__init__()
        self.response:bs = response
        self.__title = None

    def deleteFirstAndLastEmptyElements(self, array:list):
        if array[0] == '' and array[len(array)-1] == '':
            array.pop(0)
            array.pop(len(array) - 1)
        return array

    @property
    def title(self):
        if self.__title == None:
            tr:bs = self.response.find_all('tr')
            for element in tr:
                element = self.deleteFirstAndLastEmptyElements(element.get_text().split('\n'))
                if 'Аудитория' in element:
                    self.__title = element
                    break
        return self.__title

    def generateLessons(self):
        tr:bs = self.response.find_all('tr')
        formater = Formater()
        method = formater.getMethod(self.title)
        for element in tr:
            element = self.deleteFirstAndLastEmptyElements(element.get_text().split('\n'))
            if 'Аудитория' not in element:
                yield method(element)