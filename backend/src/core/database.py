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
        """Включаем pg_stat_statements и при необходимости прописываем в shared_preload_libraries"""
        async with self.pool.acquire() as conn:
            # Просто создаём расширение — оно безопасно, если уже есть
            await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements;")

            # Проверяем, есть ли уже pg_stat_statements в shared_preload_libraries
            row = await conn.fetchrow(
                "SELECT setting FROM pg_settings WHERE name = 'shared_preload_libraries'"
            )

            current_libs = row["setting"] if row and row["setting"] else ""

            if "pg_stat_statements" not in current_libs:
                # Если пусто — просто добавляем, если что-то уже есть — через запятую
                new_value = "pg_stat_statements" if not current_libs else current_libs + ",pg_stat_statements"

                await conn.execute(f"ALTER SYSTEM SET shared_preload_libraries = '{new_value}';")
                print("pg_stat_statements добавлен в shared_preload_libraries")
                print("Для применения нужен рестарт PostgreSQL (на проде — через orchestrator)")
            else:
                print("pg_stat_statements уже прописан в shared_preload_libraries")

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