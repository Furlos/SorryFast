from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.database import db
from routers.test import test_router
from routers.models import models_router


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
app.include_router(test_router)
app.include_router(models_router)
