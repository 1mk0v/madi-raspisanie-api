"""_summary_

Yields:
    _type_: _description_
"""

from bs4 import BeautifulSoup as bs
from MADI.models import *
from MADI.main import * 

class Generators:

    @staticmethod
    def schedule(html: bs):

        """
        Parsing a table with a group exam schedule
        """
        
        tr:List[bs] = html.find_all('tr')
        for element in tr:
            lesson = delete_empty_elements(element.get_text().split('\n'))
            week = element.find('th')
            if week != None and week.attrs['colspan'] == '6':
                date = remove_garbage(lesson[0])
                yield [date]
            elif len(lesson) >= 1 and 'Наименование дисциплины' not in lesson:
                yield lesson
    
    
    @staticmethod
    def exam(html: bs) -> GeneratorExit:
         
        """Parsing a table with a group class schedule"""

        tr:List[bs] = html.find_all('tr')
        for element in tr:
            exam = delete_empty_elements(element.get_text().split('\n'))
            if 'Наименование дисциплины' not in exam and len(exam) > 3:
                yield exam