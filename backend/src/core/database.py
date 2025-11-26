from __future__ import annotations

import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .config import settings


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def create_pool(self) -> None:
        """Создаём пул при старте приложения"""
        if self.pool:
            return

        self.pool = await asyncpg.create_pool(
            host=settings.pg_host,
            port=settings.pg_port,
            user=settings.pg_user,
            password=settings.pg_password,
            database=settings.pg_database,
            min_size=2,
            max_size=20,
            command_timeout=60,
        )

        await self._ensure_extensions()
        print("Подключение к PostgreSQL готово, пул создан")

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            print("Пул подключений закрыт")

    async def _ensure_extensions(self) -> None:
        """Включаем pg_stat_statements - без него нет метрик"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
                -- Чтобы статистика собиралась после рестарта
                DO $$
                BEGIN
                    IF NOT (
                        SELECT setting FROM pg_settings 
                        WHERE name = 'shared_preload_libraries' 
                        AND setting LIKE '%pg_stat_statements%'
                    ) THEN
                        ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
                        RAISE NOTICE 'Добавлено pg_stat_statements в shared_preload_libraries. Перезапустите сервер!';
                    END IF;
                END $$;
            """)

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[asyncpg.Connection, None]:
        if not self.pool:
            raise RuntimeError("Пул подключений не инициализирован! Запустите create_pool()")

        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)


db = Database()


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    async with db.acquire() as conn:
        yield conn