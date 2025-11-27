import asyncio
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import db
from routers import models_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan контекст для управления состоянием приложения"""
    print("Запуск приложения...")

    # Ждем пока PostgreSQL полностью запустится
    max_retries = 10
    retry_delay = 3

    for attempt in range(max_retries):
        try:
            await db.create_pool()
            print("✅ Подключение к PostgreSQL успешно установлено")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Попытка подключения {attempt + 1}/{max_retries} не удалась: {e}")
                print(f"🕒 Повторная попытка через {retry_delay} секунд...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"❌ Не удалось подключиться к PostgreSQL после {max_retries} попыток")
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(models_router, prefix="/api/v1", tags=["profiles"])


@app.get("/")
async def root():
    return {"message": "SorryFast API работает!", "status": "ok"}


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    try:
        # Проверяем подключение к базе данных
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