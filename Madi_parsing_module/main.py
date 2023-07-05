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
    

    def __remove_spaces(self, string:str) -> str():

        """Remove spaces from your string"""

        data = string
        while '  ' in data:
            data = data.replace('  ', ' ')
        if data[len(data)-1] == ' ':
            data = data[:-1]
        return data      


    def __remove_garbage(self, string:str, symbols:list=[]) -> str():

        """Remove garbage from your string"""

        name = string
        garbage = ['\n'] + symbols
        for simbol in garbage:
            if simbol in name:
                name = name.replace('\n','')
        name = self.__remove_spaces(name)
        return name
    


    def timetable(self, html:str) -> dict():

        """Parsing timetable of table with a group schedule"""

        timetable = dict()
        currentDay:str
        for tag in html:
            try:
                currentDay = self.__remove_garbage(tag.th.text)
                timetable[currentDay] = list()
            except:
                lesson_info:list = tag.text.split('\n')
                if lesson_info[0] == '' and lesson_info[len(lesson_info)-1] == '':
                    lesson_info.pop(0)
                    lesson_info.pop(len(lesson_info) - 1)
                if len(lesson_info) > 0 and lesson_info[0] != 'Время занятий':
                    try:
                        timetable[currentDay].append({'lesson_time': lesson_info[0],
                                                      'lesson_name': lesson_info[1],
                                                      'lesson_type': self.__remove_garbage(lesson_info[2], ['/']),
                                                      'lesson_frequency': lesson_info[3],
                                                      'auditorium': lesson_info[4],
                                                      'teacher': lesson_info[5]
                                                    })
                    except:
                        timetable[currentDay].append({'lesson_name': lesson_info[0],
                                                      'lesson_type': lesson_info[1],
                                                      'lesson_frequency': lesson_info[2]
                                                      })
        return timetable
    

    def selectors(self, html:str) -> list(): 

        """Parsing selectors of table with a group schedule"""

        data = list()
        for tag in html:
            try:
                data.append({'name': self.__remove_garbage(tag.th.text) , 'value': self.__remove_garbage(tag.td.text)})
            except:
                continue
        return data




Base_methods = MADI_PARSING_MODULE()