from fastapi import APIRouter, HTTPException
from profiles.oltp_operations import generate_oltp_report
from profiles.olap_operations import generate_olap_report
from profiles.mixed_operations import generate_mixed_report
from profiles.iot_operations import generate_iot_report
from profiles.read_intensive_operations import generate_read_intensive_report
from profiles.write_intensive_operations import generate_write_intensive_report
from profiles.web_operations import generate_web_report
from profiles.batch_operations import generate_batch_report
from core.database import db

models_router = APIRouter()

@models_router.get("/oltp_work")
async def oltp_work():
    try:
        return await generate_oltp_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/olap_work")
async def olap_work():
    try:
        return await generate_olap_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/mixed_work")
async def mixed_work():
    try:
        return await generate_mixed_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/iot_work")
async def iot_work():
    try:
        return await generate_iot_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/read_intensive_work")
async def read_intensive_work():
    try:
        return await generate_read_intensive_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/write_intensive_work")
async def write_intensive_work():
    try:
        return await generate_write_intensive_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/web_work")
async def web_work():
    try:
        return await generate_web_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/batch_work")
async def batch_work():
    try:
        return await generate_batch_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")