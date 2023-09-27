import dependencies
import madi
from database.schemas import Exam as ExamDBModel, Response_Message
from .schemas import Exam
from .utils import parseGroupExam, parseTeacherExam
from requests import exceptions
from schedule.schemas import Schedule
from database.interfaces.schedule import addToAllTableFromSchedule
from database.interfaces.exam import DBExamInfo
from groups.schemas import Exam as GroupExam, Group
from teachers.schemas import Exam as TeacherExam, Teacher
from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter(prefix='/exam', tags=['Exam'])

#---------------Group---------------#

raspisanie_groups = madi.RaspisanieGroups()
@router.get(
        "/group/{id}",
        summary = "GET group exams",
        description="By default get actual schedule for any group, but you can get old schedule",
        responses={
            status.HTTP_200_OK:{
                "model":GroupExam,
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
    })
async def getGroupExam(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_groups.get_exam(id,sem,year,name)
        return await parseGroupExam(html=html, group=Group(id=id, value=name))
    except (exceptions.ConnectionError, ValueError):
        try:
            exams = await DBExamInfo.get_by_group(id=id)
            return GroupExam(group = Group(id=id, value=name), exams = exams)
        except ValueError:
            raise HTTPException(404)
    

#---------------Teacher---------------#

raspisanie_teachers = madi.RaspisanieTeachers()

@router.get(
        "/teacher/{id}",
        summary = "GET teacher exams",
        description="By default get actual schedule for teacher, but you can get old schedule",
        responses={
            status.HTTP_200_OK:{
                "model":TeacherExam,
                "description": "OK Response",
            },
            status.HTTP_404_NOT_FOUND:{
                "description": "Response if there is no internet connection and no records in the database"
            }
    })
async def getTeacherExam(
    id:int,
    name:str = None,
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_teachers.get_exam(id, year, sem)
        return await parseTeacherExam(html=html, teacher=Teacher(id=id, value=name))
    except (exceptions.ConnectionError, ValueError) as error:
        try:
            exams = await DBExamInfo.get_by_teacher(id=id)
            return TeacherExam(teacher = Teacher(id=id, value=name), exams = exams)
        except ValueError as error:
            raise HTTPException(404, detail=error.args[0])


#---------------Exam---------------#

@router.post("/add")
async def addExam(exam:Exam) -> Response_Message:
    schedule = Schedule(date=exam.date,
                   discipline=exam.discipline,
                   type=exam.type,
                   auditorium=exam.auditorium,
                   group=exam.group,
                   teacher=exam.teacher)
    exam:ExamDBModel = await addToAllTableFromSchedule(schedule)
    id = await DBExamInfo.add(ExamDBModel(
        date_id=exam.date_id,
        discipline_id=exam.lesson_id,
        type_id=exam.type_id,
        auditorium_id=exam.auditorium_id,
        group_id=exam.group_id,
        teacher_id=exam.teacher_id)
    )
    return Response_Message(id=id)


@router.delete('/{id}/delete')
async def delExam(id:int):
    return await DBExamInfo.delete(id=id)


