from bs4 import BeautifulSoup as bs
from utils import delete_empty_elements
from typing import List

def exam(html: bs):
         
    """Parsing a table with a group class schedule"""
    tr:List[bs] = html.find_all('tr')
    for element in tr:
        exam = delete_empty_elements(element.get_text().split('\n'))
        if 'Наименование дисциплины' not in exam and len(exam) > 3:
            yield exam