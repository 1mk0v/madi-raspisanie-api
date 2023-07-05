from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import groups, schedule, exams,teachers

app = FastAPI(title='MADI ASU Terminal API')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groups.router)
app.include_router(schedule.router)
app.include_router(exams.router)
app.include_router(teachers.router)
