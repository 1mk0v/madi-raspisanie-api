from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from .departments import get_department_groups_schedule
router = APIRouter(prefix='/asu', tags=['ASU'])

from routers import request_url

ASU_ID:int = 61


@router.get('/free-audiences')
async def get_groups():
    """Returns free-audiences"""

    info = dict()

    lessons = await get_department_groups_schedule(ASU_ID)
    week_day = week_days[str(datetime.today().weekday())]

    time_now = datetime.now()

    for lesson in lessons['schedule'][week_day]:
        lesson_time = lesson['date']['time'].split(' - ')
        print((datetime.strptime(lesson_time[0]+':00',"%H:%M:%S")),  datetime.strptime(lesson_time[1]+':00', "%H:%M:%S"))
        time_to_start = datetime.strptime(lesson_time[0]+':00',"%H:%M:%S")-time_now 
        time_to_end = datetime.strptime(lesson_time[1]+':00', "%H:%M:%S")-time_now
        

    print(datetime.now().time().__str__())
    return info