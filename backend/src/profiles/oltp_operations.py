import time
from typing import Dict, Any

from core.database import Database


async def generate_oltp_report(db: Database) -> Dict[str, Any]:
    """Генерирует OLTP отчет на основе реальных метрик"""

    async with db.acquire() as conn:
        # Собираем начальные метрики
        start_wal = await conn.fetchval("SELECT pg_current_wal_lsn()")
        start_temp = await conn.fetchrow(
            "SELECT temp_files, temp_bytes FROM pg_stat_database WHERE datname = current_database()"
        )
        start_time = time.time()

        # Выполняем OLTP запросы
        operations = 0
        query_type = "UPDATE users SET money = money + 1 WHERE id = (SELECT id FROM users ORDER BY random() LIMIT 1)"

        for i in range(100):
            await conn.execute(query_type)
            operations += 1

        total_time = time.time() - start_time
        tps = operations / total_time

        # Собираем конечные метрики
        end_wal = await conn.fetchval("SELECT pg_current_wal_lsn()")
        wal_bytes = await conn.fetchval("SELECT pg_wal_lsn_diff($1, $2)", end_wal, start_wal)
        wal_mb_per_sec = (wal_bytes / 1024 / 1024) / total_time if total_time > 0 else 0

        end_temp = await conn.fetchrow(
            "SELECT temp_files, temp_bytes FROM pg_stat_database WHERE datname = current_database()"
        )
        temp_gb_per_hour = ((end_temp['temp_bytes'] - start_temp[
            'temp_bytes']) / 1024 / 1024 / 1024) / total_time * 3600 if total_time > 0 else 0

        # Другие метрики
        active_connections = await conn.fetchval("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active'")

        wait_result = await conn.fetchrow(
            "SELECT wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event IS NOT NULL LIMIT 1"
        )
        top_wait_event = f"{wait_result['wait_event_type']}: {wait_result['wait_event']}" if wait_result else "None"

        committed_percent = await conn.fetchval(
            "SELECT 100.0 * xact_commit / NULLIF(xact_commit + xact_rollback, 0) FROM pg_stat_database WHERE datname = current_database()"
        ) or 50.0

    return {
        "профиль": "Transactional OLTP",
        "причины": [
            f"DB Time Committed: {committed_percent:.1f}%",
            f"TPS: {tps:.1f}",
            f"WAL: {wal_mb_per_sec:.1f} МБ/с",
            f"Temp files: {temp_gb_per_hour:.1f} ГБ/ч"
        ],
        "метрики": {
            "tps": round(tps, 1),
            "wal_mb_per_sec": round(wal_mb_per_sec, 1),
            "temp_gb_per_hour": round(temp_gb_per_hour, 1),
            "committed_percent": round(committed_percent, 1),
            "active_connections": active_connections,
            "top_wait_event": top_wait_event
        },
        "детали_теста": {
            "время_выполнения_сек": round(total_time, 2),
            "количество_запросов": operations,
            "тип_запроса": query_type,
            "среднее_время_запроса_мс": round((total_time / operations) * 1000, 2) if operations > 0 else 0
        }
    }