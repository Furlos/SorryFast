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
            dsn=settings.db_url,
            min_size=2,
            max_size=20,
            command_timeout=60,
        )

        await self._create_tables()
        print("Подключение к PostgreSQL готово, пул создан")

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            print("Пул подключений закрыт")

    async def _create_tables(self) -> None:
        """Создание таблицы users"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            money DECIMAL(15,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
        """

        async with self.pool.acquire() as connection:
            await connection.execute(create_table_query)
            print("Таблица users создана или уже существует")

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