import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import departments, groups, teachers, schedule
from database import database

app = FastAPI(title='MADI ASU Terminal API')

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
# app.include_router(departments.router)
app.include_router(database.router)

if __name__ == '__main__':
    uvicorn.run(app) 