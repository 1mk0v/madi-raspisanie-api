from fastapi import APIRouter
from .schemas import database

router = APIRouter()


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()

