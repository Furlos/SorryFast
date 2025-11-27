from fastapi import APIRouter, HTTPException
from profiles.oltp_operations import generate_oltp_report
from core.database import db
models_router = APIRouter()
@models_router.get("/oltp_work")
async def oltp_work():
    try:
        return generate_oltp_report(db)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@models_router.get("/olap_work")
async def olap_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@models_router.get("/mixed_work")
async def mixed_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@models_router.get("/iot_work")
async def iot_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@models_router.get("/read_intensive_work")
async def read_intensive_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@models_router.get("/write_intensive_work")
async def write_intensive_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@models_router.get("/web_work")
async def web_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@models_router.get("/batch_work")
async def batch_work():
    try:
        return "Тут костыль"
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")
