from __future__ import annotations

import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import random
from datetime import datetime, timedelta

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
        await self._fill_test_data()
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
        CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
        CREATE INDEX IF NOT EXISTS idx_users_money ON users(money);
        """

        async with self.pool.acquire() as connection:
            await connection.execute(create_table_query)
            print("Таблица users создана или уже существует")

    async def _fill_test_data(self) -> None:
        """Заполнение базы тестовыми данными"""
        async with self.pool.acquire() as connection:
            # Проверяем, есть ли уже данные
            count = await connection.fetchval("SELECT COUNT(*) FROM users")

            if count >= 100000:
                print(f"✅ База уже содержит {count} записей")
                return

            print(f"🔄 Начинаем заполнение базы данных... Текущее количество записей: {count}")

            # Всегда удаляем старые данные и заполняем заново
            print("🗑️ Удаляем старые данные...")
            await connection.execute("DELETE FROM users")

            print("📝 Создаем тестовые данные...")

            # Заполняем пачками по 1000 записей для оптимизации
            batch_size = 1000
            total_records = 100000
            inserted = 0

            for batch_start in range(0, total_records, batch_size):
                batch_end = min(batch_start + batch_size, total_records)
                batch_data = []

                for i in range(batch_start, batch_end):
                    name = f"User{i}"
                    surname = f"Test{i}"
                    email = f"user{i}@test.com"  # Уникальные email
                    phone = f"+7999{str(i).zfill(7)}"  # Уникальные телефоны
                    money = round(random.uniform(0, 10000), 2)

                    batch_data.append((name, surname, email, phone, money))

                await connection.executemany(
                    """
                    INSERT INTO users (name, surname, email, phone, money)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    batch_data
                )

                inserted += len(batch_data)
                if inserted % 10000 == 0:
                    print(f"📊 Добавлено {inserted}/{total_records} записей")

            print(f"✅ Создано {inserted} тестовых записей")

    async def get_user_count(self) -> int:
        """Получить количество пользователей"""
        async with self.pool.acquire() as connection:
            return await connection.fetchval("SELECT COUNT(*) FROM users")

    async def get_random_user_id(self) -> str:
        """Получить случайный ID пользователя"""
        async with self.pool.acquire() as connection:
            return await connection.fetchval("""
                SELECT id FROM users 
                ORDER BY random() 
                LIMIT 1
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