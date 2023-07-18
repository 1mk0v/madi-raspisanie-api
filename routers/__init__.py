from datetime import datetime 

request_url = 'https://raspisanie.madi.ru/tplan/tasks/{}'

week_days = {
    "0":"Понедельник",
    "1":"Вторник",
    "2":"Среда",
    "3":"Четверг",
    "4":"Пятница",
    "5":"Суббота",
    "6":"Воскресенье",
    "7":"Полнодневные занятия"
}

def get_current_year() -> int():

    """Return current year"""

    current_academic_year:int = int(datetime.today().strftime("%Y"))-2001 
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_academic_year -= 1

    return current_academic_year


def get_current_sem() -> int():

    """Return current semester"""
    
    current_sem = 2
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_sem = 1

    return current_sem