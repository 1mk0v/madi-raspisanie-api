from models import AuditoriumInfo, Time, Community

def get_validate_auditoriums(data):
    res = dict()
    for i in data:
        lesson = i._mapping
        if lesson['auditorium'] not in res: res[lesson['auditorium']] = list()
        res[lesson['auditorium']].append(
            AuditoriumInfo(
                time=Time(
                    start=lesson['start'],
                    end=lesson['end']
                ),
                frequency=lesson['frequency'],
                weekday=lesson['weekday'],
                who_occupied=Community(
                    id=lesson['teacher_id'],
                    value=lesson['teacher_value'],
                    department_id=lesson['teacher_department_id']
                )
            )
        )
    return res
        