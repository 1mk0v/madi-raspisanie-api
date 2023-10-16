from bs4 import BeautifulSoup as bs
from utils import delete_empty_elements
from typing import List

def lesson(html: bs):

    tr:List[bs] = html.find_all('tr')
    for element in tr:
        element = delete_empty_elements(element.get_text().split('\n'))
        if 'Аудитория' not in element:
            yield element
    