from datetime import datetime, timedelta

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


def convert_to_dict_time(lesson_time:str) -> dict:
    lesson_time = lesson_time.split(' - ')
    result  = {
        "start":datetime.time(datetime.strptime(lesson_time[0],'%H:%M')) ,
        "end": datetime.time(datetime.strptime(lesson_time[0],'%H:%M') + timedelta(hours=3))
    }
    if len(lesson_time) >= 2:
        result["end"] = datetime.time(datetime.strptime(lesson_time[1],'%H:%M'))
    return result


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