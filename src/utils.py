from datetime import datetime

def get_current_year() -> int:
    current_academic_year:int = int(datetime.today().strftime("%Y"))-2000 
    current_month = int(datetime.today().strftime("%m"))
    if current_month < 9:
        current_academic_year -= 1
    return current_academic_year

def get_current_sem() -> int:
    current_sem = 2
    current_month = int(datetime.today().strftime("%m"))
    if current_month > 8:
        current_sem = 1
    return current_sem

def removeDuplicateSpaces(string: str) -> str():
    return " ".join(string.split())
