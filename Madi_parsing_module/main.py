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


class MADI_PARSING_MODULE:

    """Base methods of parsing MADI site"""

    def __init__(self):
        pass

    def remove_spaces(self, string: str) -> str():
        """Remove spaces from your string"""

        data = string
        while '  ' in data:
            data = data.replace('  ', ' ')
        if len(data) > 0 and data[len(data)-1] == ' ':
            data = data[:-1]
        return data

    def __remove_garbage(self, string: str, symbols: list = []) -> str():
        """Remove garbage from your string"""

        name = string
        garbage = ['\n'] + symbols
        for simbol in garbage:
            if simbol in name:
                name = name.replace('\n', '')
        name = self.remove_spaces(name)
        return name

        
    def exam_schedule(self, html: str) -> dict():
        """Parsing a table with a group class schedule"""

        schedule = list()
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
                    try:
                        schedule.append({'name': exam_info[0],
                                           'date': {
                                                    'day': exam_date_time[0],
                                                    'time': exam_date_time[1]
                                                   },
                                           'auditorium': exam_info[2],
                                           'teacher': exam_info[3]
                                        })
                    except Exception as error:
                        raise error

        return schedule


    def department_exam_schedule(self, html: str) -> dict():
        """Parsing a table with a ASU exam schedule"""

        schedule = list()
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
                    try:
                        schedule.append({'group': self.remove_spaces(exam_info[0]),
                                         'date':{
                                              'day':date,
                                              'time': exam_info[1]
                                          },
                                          'name': exam_info[2],
                                          'auditorium': exam_info[3],
                                          'teacher':  self.remove_spaces(exam_info[4])
                                        })
                    except Exception as error:
                        raise error

        return schedule


    def teacher_schedule(self, html: str) -> list():
        """Parsing a table with a ASU exam schedule"""

        schedule = list()
        date = 0
        for tag in html:
            try:
                if tag.b.text:
                    continue
            except:
                teacher_schedule: list = tag.text.split('\n')
                print(teacher_schedule, len(teacher_schedule))
                if teacher_schedule[0] == '' and teacher_schedule[len(teacher_schedule)-1] == '':
                    teacher_schedule.pop(0)
                    teacher_schedule.pop(len(teacher_schedule) - 1)
                if len(teacher_schedule) == 1:
                    date = teacher_schedule[0]
                if len(teacher_schedule) > 1:
                    try:
                        schedule.append({'date': {
                                           "day": date,
                                           'time': teacher_schedule[0],
                                         },
                                         'group': self.remove_spaces(teacher_schedule[1]),
                                         'name': teacher_schedule[2],
                                         'type': teacher_schedule[3],
                                         'frequency': teacher_schedule[4],
                                         'auditorium': teacher_schedule[5]
                                        })
                    except Exception as error:
                        raise error

        return schedule


    def group_schedule(self, html: str) -> dict():
        """Parsing a table with a group exam schedule"""

        timetable = list()
        currentDay: str
        for tag in html:
            try:
                currentDay = self.__remove_garbage(tag.th.text)
            except:
                lesson_info: list = tag.text.split('\n')
                if lesson_info[0] == '' and lesson_info[len(lesson_info)-1] == '':
                    lesson_info.pop(0)
                    lesson_info.pop(len(lesson_info) - 1)
                if len(lesson_info) > 0 and lesson_info[0] != 'Время занятий':
                    try:
                        timetable.append({
                            'date':{
                                'day': currentDay,
                                'time':lesson_info[0],
                            },
                            'name': lesson_info[1],
                            'type': self.__remove_garbage(lesson_info[2]),
                            'frequency': lesson_info[3],
                            'auditorium': lesson_info[4],
                            'teacher': self.remove_spaces(lesson_info[5])
                        })
                    except:
                        timetable.append({'day': lesson_info[0],
                                          'type': lesson_info[1],
                                          'frequency': lesson_info[2]
                                        })
        return timetable


    def selectors(self, html: str) -> list():
        """Parsing selectors of table with a group schedule"""

        data = list()
        for tag in html:
            try:
                data.append({'name': self.__remove_garbage(
                    tag.th.text), 'value': self.__remove_garbage(tag.td.text)})
            except:
                continue
        return data


Base_methods = MADI_PARSING_MODULE()
