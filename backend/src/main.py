import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import db
from core.metrics import collect_metrics

from routers.models import models_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan контекст для управления состоянием приложения"""
    print("Запуск приложения...")

    # Ждем 10 секунд перед подключением к PostgreSQL
    print("⏳ Ожидание запуска PostgreSQL...")
    await asyncio.sleep(10)

    try:
        await db.create_pool()
        print("✅ Подключение к PostgreSQL успешно установлено")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        raise

    print("✅ Пул подключений готов")
    yield
    await db.close()
    print("✅ Приложение завершено")


app = FastAPI(
    title="SorryFast API",
    description="API для анализа профилей нагрузки PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)
@app.get("/debug/metrics")
async def debug_metrics():
    metrics = await collect_metrics()
    return {
        "время": datetime.now().strftime("%H:%M:%S"),
        "метрики": metrics,
        "статус": "работает"
    }

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(models_router)


@app.get("/")
async def root():
    return {"message": "SorryFast API работает!", "status": "ok"}


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    try:
        user_count = await db.get_user_count()
        return {
            "status": "healthy",
            "database": "connected",
            "users_count": user_count,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time()
        }