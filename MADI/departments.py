from .main import remove_spaces, remove_garbage
from .models import *

class Department:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def exam_schedule(html: str, department_name:str = None) -> Exam_Info:

        """Parsing a table with a ASU exam schedule"""

        data = Exam_Info(name=department_name, exam=list())
        date = 0
        for tag in html:
            try:
                if tag.b.text:
                    continue
            except:
                exam_info: list = tag.text.split('\n')
                if exam_info[0] == '' and exam_info[len(exam_info)-1] == '':
                    exam_info.pop(0)
                    exam_info.pop(len(exam_info) - 1)
                if len(exam_info) == 1:
                    date = exam_info[0]
                if len(exam_info) > 1:
                    data.exam.append(Schedule(
                        date=Date(
                            day=date,
                            time=exam_info[1]
                        ),
                        group=remove_spaces(exam_info[0]),
                        discipline=exam_info[2],
                        auditorium=exam_info[3],
                        teacher= remove_spaces(exam_info[4])
                    ))
        return data


    @staticmethod
    def groups_schedule(html: str, department_name:str = None) -> Schedule_Info:
        data = Schedule_Info(name=department_name, schedule=dict())
        date = 0
        for tag in html:
            try:
                if tag.b.text:
                    continue
            except:
                schedule:list = tag.text.split('\n')
                if schedule[0] == '' and schedule[len(schedule)-1] == '':
                    schedule.pop(0)
                    schedule.pop(len(schedule) - 1)
                if len(schedule) == 1:
                    date = remove_garbage(schedule[0])
                    data.schedule[date] = list()
                if len(schedule) > 1:
                    data.schedule[date].append(Schedule(
                        date=Date(
                            time=schedule[0],
                            friequency=schedule[1]
                        ),
                        auditorium=schedule[2],
                        group=remove_spaces(schedule[3]),
                        discipline=schedule[4],
                        teacher=remove_spaces(schedule[5])
                    ))   
        return data
    

    @staticmethod
    def groups(html: str) -> list:
        groups = list()
        for tag in html:
            try:
                if tag.b.text:
                    continue
            except:
                data: list = tag.text.split('\n')
                if len(data) > 1:
                    try:
                        group = remove_spaces(data[4])
                        if group not in groups:
                            groups.append(group)
                    except:
                        continue     
        return groups
