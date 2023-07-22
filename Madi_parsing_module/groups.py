from bs4 import BeautifulSoup as bs
from .models import *
from .main import delete_empty_elements, remove_garbage, remove_spaces



class Group:

    """
        Parsing methods for group object
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    def __init__(self) -> None:
        pass


    @staticmethod
    def schedule(html: bs, group_name: str = None) -> Schedule_Info:
        #TODO

        """
        Parsing a table with a group exam schedule
        """
        
        data = Schedule_Info(name=group_name, schedule={})
        date:str
        full_day_lesson:str
        tr:List[bs] = html.find_all('tr')
        for element in tr:
            lesson = delete_empty_elements(element.get_text().split('\n'))
            week = element.find('th')
            if week != None and week.attrs['colspan'] == '6':
                date = remove_garbage(lesson[0])
                data.schedule[date] = list()
            if len(lesson) > 4 and lesson[0] != 'Время занятий':
                data.schedule[date].append(Schedule(
                    date=Date(
                        time=lesson[0],
                        friequency=lesson[3]
                    ),
                    discipline=lesson[1],
                    type=remove_garbage(lesson[2]),
                    auditorium=lesson[4],
                    teacher=remove_garbage(lesson[5])
                    )
                )
            elif len(lesson) == 3:
                data.schedule[date].append(Schedule(
                    date=Date(
                        friequency=lesson[2],
                        day=lesson[0]
                        ),
                    discipline=lesson[1]
                    )
                )
            else:
                week = element.find('td')
                if len(lesson) == 4 and week != None:
                    full_day_lesson = lesson[0]
                    data.schedule[date].append(Schedule(
                    date=Date(
                        friequency=lesson[2],
                        day=full_day_lesson
                        ),
                    discipline=[lesson[1]]
                    ))
                elif len(lesson) == 1 and week != None:
                    data.schedule[date][len(data.schedule[date])-1].discipline.append(lesson[0])
                       
        return data


    @staticmethod
    def exam_schedule(html: str, group_name:str = None) -> Exam_Info:
        """Parsing a table with a group class schedule"""

        data = Exam_Info(name=group_name, exam=list())
        for tag in html:
            try:
                if tag.th.text:
                    continue
            except:
                exam_info: list = tag.text.split('\n')
                if exam_info[0] == '' and exam_info[len(exam_info)-1] == '':
                    exam_info.pop(0)
                    exam_info.pop(len(exam_info) - 1)
                if len(exam_info) > 0:
                    exam_date_time = exam_info[1].split(' ')
                    data.exam.append(Schedule(
                        date=Date(
                            day=exam_date_time[0],
                            time=exam_date_time[1]
                            ),
                        discipline=exam_info[0],
                        auditorium=exam_info[2],
                        teacher=remove_garbage(exam_info[3], ['..'])
                    ))

        return data