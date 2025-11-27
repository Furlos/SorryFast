import time
from typing import Dict, Any
from decimal import Decimal
from core.database import Database

async def generate_oltp_report(db: Database) -> Dict[str, Any]:
    """Генерирует OLTP отчет"""
    try:
        async with db.acquire() as conn:
            start_wal = await conn.fetchval("SELECT pg_current_wal_lsn()")
            start_temp = await conn.fetchrow(
                "SELECT temp_bytes FROM pg_stat_database WHERE datname = current_database()")
            start_time = time.time()

            operations = 0
            for i in range(100):
                await conn.execute(
                    "UPDATE users SET money = money + 1 WHERE id = (SELECT id FROM users ORDER BY random() LIMIT 1)")
                operations += 1

            total_time = time.time() - start_time
            tps = operations / total_time

            end_wal = await conn.fetchval("SELECT pg_current_wal_lsn()")
            wal_bytes = float(await conn.fetchval("SELECT pg_wal_lsn_diff($1, $2)", end_wal, start_wal))
            wal_mb_per_sec = (wal_bytes / 1024 / 1024) / total_time if total_time > 0 else 0

            end_temp = await conn.fetchrow("SELECT temp_bytes FROM pg_stat_database WHERE datname = current_database()")
            start_temp_bytes = float(start_temp['temp_bytes']) if start_temp and start_temp['temp_bytes'] else 0
            end_temp_bytes = float(end_temp['temp_bytes']) if end_temp and end_temp['temp_bytes'] else 0
            temp_gb_per_hour = ((end_temp_bytes - start_temp_bytes) / 1024 / 1024 / 1024) / total_time * 3600 if total_time > 0 else 0

            active_connections = await conn.fetchval("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active'")

            db_stats = await conn.fetchrow(
                "SELECT xact_commit, xact_rollback FROM pg_stat_database WHERE datname = current_database()")
            xact_commit = float(db_stats['xact_commit']) if db_stats and db_stats['xact_commit'] else 0
            xact_rollback = float(db_stats['xact_rollback']) if db_stats and db_stats['xact_rollback'] else 0
            committed_percent = (100.0 * xact_commit / (xact_commit + xact_rollback)) if (xact_commit + xact_rollback) > 0 else 95.0

        return {
            "профиль": "Transactional OLTP",
            "метрики": {
                "tps": round(tps, 1),
                "latency_ms": round((total_time / operations) * 1000, 2),
                "throughput_mb_sec": round(wal_mb_per_sec, 1),
                "committed_percent": round(committed_percent, 1),
                "temp_gb_per_hour": round(temp_gb_per_hour, 1),
                "active_connections": active_connections
            }
        }
    except Exception:
        return {
            "профиль": "PROBLEM"
        }