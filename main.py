import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import db_methods, departments, groups, teachers, schedule
from database import database

app = FastAPI(
    title='MADI SCHEDULE API',
    description="""
MADI SCHEDULE API

## Teachers

* You can get **list of teachers info**.\n
* You can get **list of teacher schedule info**.\n
* You can add **teacher info**.\n
* You can delete **teacher info**.\n

## Groups

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

app.include_router(teachers.router)
app.include_router(groups.router)
app.include_router(schedule.router)
app.include_router(db_methods.router)
# app.include_router(departments.router)
app.include_router(database.router)

if __name__ == '__main__':
    uvicorn.run(app) 