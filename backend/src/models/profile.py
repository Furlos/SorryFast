from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


ProfileName = Literal[
    "Classic OLTP",
    "Analytical OLAP",
    "Write-heavy IoT & Telemetry",
    "Mixed OLTP + Periodic Analytics",
    "High-Concurrency Web/API",
    "Financial-Safe OLTP",
    "Read-Heavy / In-Memory Cache",
    "Batch/ETL & Night Loads"
]

@dataclass(frozen=True)
class LoadProfile:
    id: int
    name: ProfileName
    description: str

    committed_min: int | None = None
    committed_max: int | None = None
    tps_min: float | None = None
    wal_mb_sec_min: float | None = None
    temp_gb_per_hour_min: float | None = None
    connections_min: int | None = None




PROFILES = [
    LoadProfile(1, "Classic OLTP", "Платежи, переводы, бронирование", committed_min=70, tps_min=500),
    LoadProfile(2, "Analytical OLAP", "Отчёты, BI, витрины", committed_max=30, temp_gb_per_hour_min=10),
    LoadProfile(3, "Write-heavy IoT & Telemetry", "TimescaleDB, миллионы INSERT", wal_mb_sec_min=150),
    LoadProfile(4, "Mixed OLTP + Periodic Analytics", "День — платежи, ночь — отчёты", committed_min=40, committed_max=70),
    LoadProfile(5, "High-Concurrency Web/API", "Мобильное приложение, API", connections_min=2000),
    LoadProfile(6, "Financial-Safe OLTP", "Core-banking, zero data loss", committed_min=90),
    LoadProfile(7, "Read-Heavy / In-Memory Cache", "Рекомендации, кэш", committed_max=20),
    LoadProfile(8, "Batch/ETL & Night Loads", "Загрузки из Kafka, миграции", temp_gb_per_hour_min=50),
]