import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groups.router import router as group_router
from teachers.router import router as teacher_router
from schedule.router import router as schedule_router
from departments.router import router as department_router
from other.db_methods import router as other_router
from database import database

app = FastAPI(
    title='MADI SCHEDULE API',
    description="""
## Teachers

* You can get **list of teachers info**.\n
* You can get **list of teacher schedule info**.\n
* You can add **teacher info**.\n
* You can delete **teacher info**.\n

## Groups

* С каждым годом ID групп обновляются, поэтому вы не сможете найти расписание, к примеру, \
за прошлый год операясь на актуальный ID искомой группы.
* You can get **list of groups info**.\n
* You can get **list of group schedule info**.\n
* You can add **group info**.\n
* You can delete **group info**.\n""",
    contact={
        "name": "Potapchuk Danila Antonovich",
        "url": "https://t.me/nivicki",
        "email": "potapchuk01@mail.ru",
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(department_router)
app.include_router(teacher_router)
app.include_router(group_router)
app.include_router(schedule_router)
app.include_router(other_router) #TODO есть ли смысл ее оставлять?
app.include_router(database.router)

if __name__ == '__main__':
    uvicorn.run(app) 