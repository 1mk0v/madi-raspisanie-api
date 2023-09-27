from fastapi import APIRouter
from .schemas import database as db

router = APIRouter()

@router.on_event("startup")
async def startup():
    await db.connect()

@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()

