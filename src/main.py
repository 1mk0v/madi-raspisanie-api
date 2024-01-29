from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groups.router import router as group_router
from teachers.router import router as teacher_router
from schedule.router import router as schedule_router
from exam.router import router as exam_router
from department.router import router as department_router
from auditoriums.router import router as auditoriumRouter
from database import database

app = FastAPI(
    title='MADI SCHEDULE API',
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

app.include_router(auditoriumRouter)
app.include_router(department_router)
app.include_router(teacher_router)
app.include_router(group_router)
app.include_router(schedule_router)
app.include_router(exam_router)
app.include_router(database.router)
