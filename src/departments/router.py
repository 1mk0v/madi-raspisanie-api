from madi import RaspisanieDepartments
from requests.exceptions import ConnectionError
from dependencies import current_sem, current_year
from teachers.utils import find_by_names
from utils import remove_garbage
from models import Department
from fastapi import APIRouter, HTTPException, Depends
from typing import List

router = APIRouter(prefix='/departments', tags=['Departments'])

raspisanie_departments = RaspisanieDepartments()

@router.get('/')
async def get_departemnts() -> List[Department]:

    """Returns departments of MADI"""

    data = list()
    try:
        html = await raspisanie_departments.get()
    except (ConnectionError,ValueError):
        try:
            raise HTTPException(502)
        except ValueError:
            raise HTTPException(404)
    for element in html:
        if '20' not in element.text and int(element['value']) > 0:
            data.append(Department(
                id=element['value'],
                value=remove_garbage(element.text)
                )
            )
    return data

@router.get('/{id}/teachers')
async def get_departemnt_teachers(
    id:int,
    sem = Depends(current_sem),
    year = Depends(current_year)
):
    try:
        html = await raspisanie_departments.get_teachers(
            id=id,
            sem=sem,
            year=year
        )
    except (ConnectionError, ValueError):
        try:
            raise HTTPException(502)
        except ValueError:
            raise HTTPException(404)
     
    return await find_by_names(
        teachers=[element.text for element in html],
        dep_id=id
    )

# @router.get('/{id}/auditoriums')
# async def get_department_auditoriums(id:int,
#                                      sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
#                                      year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
#     response = requests.post(request_url.format("tableFiller.php"),
#                              data={'tab': '11',
#                                    'kf_id': f'{id}',
#                                    'sort': '2',
#                                    'tp_year': f'{year}',
#                                    'sem_no': f'{sem_number}'})
    
#     html = bs(response.text, 'lxml')
#     table = html.find_all('table')
    
#     if len(table) < 1:
#         raise HTTPException(404, detail=html.text)
    
#     auditoriums = list()

#     for info in table[1]:
#         try:
#             auditorium = info.text.split('\n')[3]
#             if int(auditorium[:3]) and auditorium not in auditoriums:
#                 auditoriums.append(auditorium)
#         except:
#             continue
    
#     if len(auditoriums) == 0:
#         raise HTTPException(404)

#     return {'auditoriums':auditoriums}


# @router.get('/{id}/groups')
# async def get_department_groups(id:int,
#                                 sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
#                                 year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()) -> list:
    
#     response = requests.post(request_url.format("tableFiller.php"),
#                              data={'tab': '11',
#                                    'kf_id': f'{id}',
#                                    'sort': '2',
#                                    'tp_year': f'{year}',
#                                    'sem_no': f'{sem_number}'})
    
#     html = bs(response.text, 'lxml')
#     table = html.find_all('table')
    
#     schedule = list()
#     if len(table) > 0:
#         schedule = Department.groups(table[1])
  
#     return schedule


# @router.get('/{id}/schedule')
# async def get_department_groups_schedule(id:int,
#                                         sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
#                                         year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()):
    
#     response = requests.post(request_url.format("tableFiller.php"),
#                              data={'tab': '11',
#                                    'kf_id': f'{id}',
#                                    'sort': '2',
#                                    'tp_year': f'{year}',
#                                    'sem_no': f'{sem_number}'})
    
#     html = bs(response.text, 'lxml')
#     table = html.find_all('table')
    
#     if len(table) < 1:
#         raise HTTPException(404, detail=html.text)
    
#     schedule = Department.groups_schedule(table[1])

#     return schedule


# @router.get('/{id}/exams')
# async def get_departemnt_exams(
#     id:int = 61,
#     sem_number:Annotated[int, Path(ge=1, le=2)] = get_current_sem(),
#     year: Annotated[int, Path(ge=19, le=get_current_year())] = get_current_year()
#     ):
    
#     """Returns JSON exams of department"""

#     response = requests.post(request_url.format("tableFiller.php"),
#                              data={'tab': '10',
#                                    'kf_id': f'{id}',
#                                    'sort': '1',
#                                    'tp_year': f'{year}',
#                                    'sem_no': f'{sem_number}'})
    
#     html = bs(response.text, 'lxml')
#     tables = html.find_all('table')

#     if len(tables) <= 1 :
#         p = html.find_all('p')
#         raise HTTPException(404, detail=p[0].text)

#     data = Department.exam_schedule(html=tables[1])

#     return data.dict(exclude_none=True)