from fastapi import APIRouter, HTTPException
from profiles.oltp_operations import generate_oltp_report
from core.database import db

models_router = APIRouter()

@models_router.get("/oltp_work")
async def oltp_work():
    try:
        # Добавьте await здесь
        return await generate_oltp_report(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/olap_work")
async def olap_work():
    try:
        # Заглушка для OLAP
        return {
            "профиль": "Analytical OLAP",
            "причины": ["Тяжелые аналитические запросы", "Много временных файлов"],
            "метрики": {"tps": 10, "latency_ms": 1500, "throughput_mb_sec": 45.5}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/mixed_work")
async def mixed_work():
    try:
        return {
            "профиль": "Mixed OLTP+OLAP",
            "причины": ["Смешанная нагрузка", "Умеренный TPS"],
            "метрики": {"tps": 250, "latency_ms": 120, "throughput_mb_sec": 25.3}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/iot_work")
async def iot_work():
    try:
        return {
            "профиль": "IoT Workload",
            "причины": ["Много INSERT операций", "Высокий объем данных"],
            "метрики": {"tps": 800, "latency_ms": 80, "throughput_mb_sec": 65.7}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/read_intensive_work")
async def read_intensive_work():
    try:
        return {
            "профиль": "Read-Intensive",
            "причины": ["Преобладание SELECT запросов", "Высокий cache hit ratio"],
            "метрики": {"tps": 400, "latency_ms": 45, "throughput_mb_sec": 15.2}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/write_intensive_work")
async def write_intensive_work():
    try:
        return {
            "профиль": "Write-Intensive",
            "причины": ["Много INSERT/UPDATE операций", "Высокий WAL объем"],
            "метрики": {"tps": 600, "latency_ms": 95, "throughput_mb_sec": 85.1}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/web_work")
async def web_work():
    try:
        return {
            "профиль": "Web Service",
            "причины": ["Короткие транзакции", "Высокая параллельность"],
            "метрики": {"tps": 1200, "latency_ms": 25, "throughput_mb_sec": 18.9}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

@models_router.get("/batch_work")
async def batch_work():
    try:
        return {
            "профиль": "Batch Processing",
            "причины": ["Пакетная обработка", "Длительные транзакции"],
            "метрики": {"tps": 50, "latency_ms": 2000, "throughput_mb_sec": 120.5}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")