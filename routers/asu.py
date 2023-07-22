from fastapi import APIRouter
from datetime import datetime, timedelta
from .departments import get_department_groups_schedule
from .groups import get_groups as get_groups_ids
from .groups import get_group_schedule
from .teachers import get_all_teachers
router = APIRouter(prefix='/asu', tags=['ASU'])
from bs4 import BeautifulSoup as bs 
from routers import week_days, request_url
import requests
ASU_ID = 61


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


@router.get('/test')
async def get_test():


    groups = await get_all_teachers()

    for id in groups:
        try:
  
            response = requests.post(request_url.format("tableFiller.php"),
                             data={'tab': '8',
                                   'tp_year': f'{2}',
                                   'sem_no': f'{22}',
                                   'pr_id': f'{id}'})
            with open(f'tmp/teacher/exam/exam_{id}.txt', 'w+') as f:
                f.write(response.text)
                f.close

            print(id, "success")
        except Exception as e:
            print(e)
            print(id, "fail")

    return {'message':'ok'}

