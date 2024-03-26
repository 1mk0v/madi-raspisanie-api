from fastapi import APIRouter, HTTPException, Depends
from bridges.institutes_requests import madi as madiRequests
from models import Response, ResponseWithCommunity, Community
from database import schemas, database
from bridges import madi, Generator
from requests import exceptions as requests_exc
from utils import get_current_year
import exceptions as exc
import dependencies

router = APIRouter(prefix='/teacher', tags=['Communities'])
raspisanie_teachers = madiRequests.RaspisanieTeachers()
teacherTable = database.DatabaseInterface(table=schemas.Teacher, engine=database.async_engine)

@router.get(
    '/',
    summary = "GET actual teachers",
    response_model=ResponseWithCommunity
)
async def get_all_teachers(
    sem = Depends(dependencies.current_sem),
    year = Depends(dependencies.current_year)
):
    try:
        html = await raspisanie_teachers.get(year, sem)
        generator = Generator(madi.MADIBridge(html))
        return await generator.generateListOfCommunity()
    except (requests_exc.ConnectionError, exc.NotFoundError) as error:
        try:
            query = teacherTable.base_query.where(
                teacherTable.table.year == get_current_year()
            )
            db_result = (await teacherTable._execute_query(query)).all()
            data = [Community.model_validate(row._mapping) for row in db_result]
            return Response(data=data)
        except exc.NotFoundError as error:
            raise HTTPException(error.status_code, detail=error.detail)