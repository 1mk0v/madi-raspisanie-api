import config
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from groups.router import router as group_router
from teachers.router import router as teacher_router
from events.router import router as events_router
from department.router import router as department_router
from auditoriums.router import router as auditoriumRouter

app = FastAPI(
    title='API Расписание МАДИ',
    contact={
        "name": "Данила Антонович",
        "url": "https://t.me/nivicki",
        "email": "potapchuk01@mail.ru",
    },
    version='0.2.1',
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },

)
app.openapi_version = "3.0.2"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print("Time took to process the request and return response is {} sec".format(time.time() - start_time))
    return response

app.include_router(auditoriumRouter)
app.include_router(department_router)
app.include_router(group_router)
app.include_router(teacher_router)
app.include_router(events_router)


@app.on_event('startup')
async def startup_event():
    from database.database import create_database
    create_database()