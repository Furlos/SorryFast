from typing import TypedDict

from .database import db


class CurrentMetrics(TypedDict):
    tps: float
    wal_mb_per_sec: float
    temp_gb_per_hour: float
    commited_percent: float
    active_connections: int
    top_wait_event: str


async def collect_metrics() -> CurrentMetrics:
    async with db.acquire() as conn:
        stats = await conn.fetchrow("""
            SELECT 
                calls,
                total_exec_time,
                temp_blks_written,
                wal_bytes
            FROM pg_stat_statements
            ORDER BY calls DESC LIMIT 1
        """)

        if not stats or stats["calls"] is None:
            return {
                "tps": 0.0,
                "wal_mb_per_sec": 0.0,
                "temp_gb_per_hour": 0.0,
                "committed_percent": 0.0,
                "active_connections": 0,
                "top_wait_event": "нет данных"
            }
        minutes = 10.0
        tps = stats["calls"] / (minutes * 60)
        wal_mb_per_sec = (stats["wal_bytes"] or 0) / (1024 * 1024) / (minutes * 60)
        temp_gb_per_hour = (stats["temp_blks_written"] or 0) * 8192 / (1024 ** 3) * (60 / minutes)

        # Берём из pg_stat_activity (примерно)
        activity = await conn.fetchrow("""
                    SELECT 
                        count(*) as total,
                        sum(CASE WHEN state = 'active' THEN 1 ELSE 0 END) as active
                    FROM pg_stat_activity
                    WHERE backend_type = 'client backend'
                """)
        committed_percent = 0.0
        if activity and activity["total"] > 0:
            commited_percent = round((activity["active"] / activity["total"]) * 100, 1)

        connections = await conn.fetchval("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")

        wait = await conn.fetchval("""
            SELECT wait_event_type || ': ' || wait_event 
            FROM pg_stat_activity 
            WHERE wait_event IS NOT NULL 
            GROUP BY wait_event_type, wait_event 
            ORDER BY count(*) DESC LIMIT 1
        """)

        return {
            "tps": round(tps, 1),
            "wal_mb_per_sec": round(wal_mb_per_sec, 2),
            "temp_gb_per_hour": round(temp_gb_per_hour, 2),
            "committed_percent": committed_percent,
            "active_connections": int(connections or 0),
            "top_wait_event": wait or "CPU"}
