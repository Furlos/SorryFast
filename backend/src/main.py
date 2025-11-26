from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi import Query

from .core.database import db
from .core.fake_metrics import generate_fake_metrics
from .core.metrics import collect_metrics
from .models.profile import PROFILES


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения...")
    await db.create_pool()
    print("Пул подключений готов, pg_stat_statements включен")
    yield

    print("Остановка приложения...")
    await db.close()
    print("Все подключения закрыты")


app = FastAPI(title="VTB Load Profile Analyzer", lifespan=lifespan)


@app.get("/debug/metrics")
async def debug_metrics():
    metrics = await collect_metrics()
    return {
        "время": datetime.now().strftime("%H:%M:%S"),
        "метрики": metrics,
        "статус": "работает"
    }


@app.get("/profile/{profile_name}")
async def current_profile(db: str = Query("prodbill01", description="Имя базы")):
    # Находим профиль по имени базы (как в демо-боте)
    demo_map = {
        "prodbill01": "Financial-Safe OLTP",
        "analytics01": "Analytical OLAP",
        "iot-sensors": "Write-heavy IoT & Telemetry",
        "mobile-api": "High-Concurrency Web/API",
        "billing-night": "Batch/ETL & Night Loads",
        "mixed01": "Mixed OLTP + Periodic Analytics",
        "cache01": "Read-Heavy / In-Memory Cache",
        "default": "Classic OLTP"
    }

    profile_name = demo_map.get(db.split()[0], demo_map["default"])
    profile = next(p for p in PROFILES if p.name == profile_name)

    # Генерируем ЖИВЫЕ фейковые метрики — каждый запрос новые!
    metrics = generate_fake_metrics(profile_name)

    return {
        "база": db,
        "профиль": profile.name,
        "совпадение": "99%",
        "причины": [
            f"DB Time Committed: {metrics['committed_percent']}%",
            f"TPS: {metrics['tps']:,}",
            f"WAL: {metrics['wal_mb_per_sec']} МБ/с",
            f"Temp files: {metrics['temp_gb_per_hour']} ГБ/ч"
        ],
        "рекомендация": "Включить Financial-Safe режим" if "Financial" in profile.name else "Оптимально",
        "метрики": metrics
    }


@app.get("/demo/profile")
async def demo_profile():
    import random
    db_names = ["prodbill01", "analytics01", "iot-sensors", "mobile-api", "billing-night"]
    db = random.choice(db_names)
    return await current_profile(db)