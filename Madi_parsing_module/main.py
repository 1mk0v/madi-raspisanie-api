############################################################################################################
#                                                                                                          #
#                                                                                                          #
#                                           ED.                                                            #
#                                           E#Wi                                          .  :             #
#                                           E###G.        t                              ;W  Ef            #
#                ..       :             ..  E#fD#W;       Ej                 ..         f#E  E#t           #
#               ,W,     .Et            ;W,  E#t t##L      E#,               ;W,       .E#f   E#t           #
#              t##,    ,W#t           j##,  E#t  .E#K,    E#t              j##,      iWW;    E#t           #
#             L###,   j###t          G###,  E#t    j##f   E#t             G###,     L##Lffi  E#t fi        #
#           .E#j##,  G#fE#t        :E####,  E#t    :E#K:  E#t           :E####,    tLLG##L   E#t L#j       #
#          ;WW; ##,:K#i E#t       ;W#DG##,  E#t   t##L    E#t          ;W#DG##,      ,W#i    E#t L#L       #
#         j#E.  ##f#W,  E#t      j###DW##,  E#t .D#W;     E#t         j###DW##,     j#E.     E#tf#E:       #
#       .D#L    ###K:   E#t     G##i,,G##,  E#tiW#G.      E#t        G##i,,G##,   .D#j       E###f         #
#      :K#t     ##D.    E#t   :K#K:   L##,  E#K##i        E#t      :K#K:   L##,  ,WK,        E#K,          #
#      ...      #G      ..   ;##D.    L##,  E##D.         E#t     ;##D.    L##,  EG.         EL            #
#               j            ,,,      .,,   E#t           ,;.     ,,,      .,,   ,           :             #
#                                           L:                                                             #
#                                                                                                          #
#                                                                                                          #
#                                        Developed by Potapchuk D.A.                                       #
#                                                                                                          #
############################################################################################################

from .models import *


def remove_spaces(string: str) -> str():

    """Return your input string without double spaces"""

    data = string
    while '  ' in data:
        data = data.replace('  ', ' ')
    if len(data) > 0 and data[len(data)-1] == ' ':
        data = data[:-1]
    return data


def remove_garbage(string: str, symbols: list = []) -> str():

    """Remove garbage from your string"""
    
    name = string
    garbage = ['\n'] + symbols
    for simbol in garbage:
        if simbol in name:
            name = name.replace(simbol, '')
    name = remove_spaces(name)
    return name


def set_selectors(html: str) -> list():

    """Parsing selectors of table with a group schedule"""
    
    data = list()
    for tag in html:
        try:
            data.append({'name': remove_garbage(tag.th.text),
                         'value':remove_garbage(tag.td.text)})
        except:
            continue
    return data



class Teacher:
    
    def __init__(self) -> None:
        pass


    @staticmethod
    def exam_schedule(html: str, teacher_name:str = None) -> Exam_Info:

        """Parsing a table with a group class schedule"""

        data = Exam_Info(name=teacher_name ,exam=list())
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
                        group=exam_info[0],
                        discipline=exam_info[3],
                        auditorium=exam_info[2]
                    ))

        return data


    @staticmethod
    def get_schedule(html: str, teacher_name:str = None) -> Schedule_Info:

        """Parsing a table with a ASU exam schedule"""

        data = Schedule_Info(sorted_by=teacher_name ,schedule={})
        date = 0
        for tag in html:
            try:
                if tag.b.text:
                    continue
            except:
                schedule: list = tag.text.split('\n')
                if schedule[0] == '' and schedule[len(schedule)-1] == '':
                    schedule.pop(0)
                    schedule.pop(len(schedule) - 1)
                if len(schedule) == 1:
                    date = remove_garbage(schedule[0])
                    data.schedule[date] = list()
                if len(schedule) > 1:
                    data.schedule[date].append(Schedule(
                        group=remove_spaces(schedule[1]),
                        discipline=schedule[2],
                        date=Date(
                            friequency=schedule[4],
                            time=schedule[0]
                        ),
                        type=schedule[3],
                        auditorium=schedule[5]))
        return data


class Group:

    """
        Parsing methods for group object
    """
    def __init__(self) -> None:
        pass


    @staticmethod
    def schedule(html: str, group_name: str = None) -> Schedule_Info:
        #TODO
        """
        Parsing a table with a group exam schedule \n
        Have error on 8744 8745 8746 8748 ID's
        """

        data = Schedule_Info(name=group_name, schedule={})
        currentDay: str
        for tag in html:
            try:
                currentDay = remove_garbage(tag.th.text)
                data.schedule[currentDay] = list()
            except:
                schedule:list = tag.text.split('\n')
                if schedule[0] == '' and schedule[len(schedule)-1] == '':
                    schedule.pop(0)
                    schedule.pop(len(schedule) - 1)
                if len(schedule) > 1 and schedule[0] != 'Время занятий':
                    try:
                        data.schedule[currentDay].append(Schedule(
                            date=Date(
                                time=schedule[0],
                                friequency=schedule[3]
                            ),
                            discipline=schedule[1],
                            type=remove_garbage(schedule[2]),
                            auditorium=schedule[4],
                            teacher=remove_spaces(schedule[5])
                            )
                        )
                    except:
                        data.schedule[currentDay].append(Schedule(
                            date=Date(
                                friequency=schedule[2],
                                day=schedule[0]
                            ),
                            discipline=schedule[1]
                        )
                    )
                    # else:
                    #     print(schedule)
                    #     if len(schedule) == 1:
                    #         length = len(data.schedule[currentDay]) - 1
                    #         if type(data.schedule[currentDay][length].discipline) == str:
                    #             added_discipline = data.schedule[currentDay][length].discipline
                    #             data.schedule[currentDay][length].discipline = list(added_discipline)
                    #         else:
                    #             data.schedule[currentDay][length].discipline.append(schedule[0])
                       
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
