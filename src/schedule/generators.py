from bs4 import BeautifulSoup as bs
from utils import remove_garbage
from typing import List 
from .utils import delete_empty_elements


def lesson(html: bs):

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
    

def exam(html: bs):
         
        """Parsing a table with a group class schedule"""

        tr:List[bs] = html.find_all('tr')
        for element in tr:
            exam = delete_empty_elements(element.get_text().split('\n'))
            if 'Наименование дисциплины' not in exam and len(exam) > 3:
                yield exam