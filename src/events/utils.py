from models import LessonInfo, Community, Time

def get_validate_event(data):
    res = []
    for item in data:
        event = item._mapping
        group = Community(
            id=event['group_id'],
            department_id=event['group_department_id'],
            value=event['group_value']
        )
        teacher = Community(
            id=event['teacher_id'],
            department_id=event['teacher_department_id'],
            value=event['teacher_value']
        )
        time = Time(
            start=event['start'],
            end=event['end']
        )
        lesson = LessonInfo.model_validate(event)
        lesson.time = time
        lesson.group = group
        lesson.teacher = teacher
        res.append(lesson)
    return res
