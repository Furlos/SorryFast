from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from .core.database import db
from .core.metrics import collect_metrics


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



@app.get("/")
async def root():
    return {"message": "PostgreSQL Profile Analyzer готов к работе", "docs": "/docs", "status": "OK"}


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}



@app.get("/debug/metrics")
async def debug_metrics():
    metrics = await collect_metrics()
    return {
        "время": datetime.now().strftime("%H:%M:%S"),
        "метрики": metrics,
        "статус": "работает"
    }
