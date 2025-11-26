from typing import NamedTuple
from ..models.profile import PROFILES, LoadProfile
from .metrics import collect_metrics, CurrentMetrics

class DetectionResult(NamedTuple):
    profile: LoadProfile
    match_score: int
    reasons: list[str]


DEMO_MODE = True #False на проде


async def detect_profile(db_name: str = "prodbill01") -> DetectionResult:
    # Если демо, то просто крутим рулетку по именам баз
    if DEMO_MODE:
        demo_profiles = [
            ("prodbill01", PROFILES[5], 96, ["Committed ≥ 90%", "TPS ≥ 500"]),  # Financial-Safe OLTP
            ("analytics01", PROFILES[1], 94, ["Committed ≤ 30%", "temp_files ≥ 50 ГБ/ч"]),  # Analytical OLAP
            ("iot-sensors", PROFILES[2], 99, ["WAL ≥ 300 МБ/с"]),  # Write-heavy IoT
            ("mobile-api", PROFILES[4], 92, ["соединений ≥ 4000"]),  # High-Concurrency
            ("billing-night", PROFILES[7], 88, ["temp_files ≥ 80 ГБ/ч"]),  # Batch/ETL
        ]

        # По имени базы выдаём нужный профиль
        for name, profile, score, reasons in demo_profiles:
            if name in db_name:
                return DetectionResult(profile, score, reasons)

        return DetectionResult(PROFILES[3], 90, ["Committed ≥ 40%", "Committed ≤ 70%"])


    metrics = await collect_metrics()

    best_profile = PROFILES[0]  # Classic OLTP — дефолт для банков
    best_score = 30             # базовые 30% — «похоже на OLTP»
    reasons = ["По умолчанию — банковская нагрузка (OLTP)"]

    # Если вообще нет активности, то сразу возвращаем Classic OLTP с пояснением
    if metrics["active_connections"] == 0 and metrics["tps"] < 1:
        return DetectionResult(
            profile=best_profile,
            match_score=85,
            reasons=["База только стартовала", "Нет активных запросов", "Предполагаем Classic OLTP"]
        )

    # Если есть хоть какая-то активность, то считаем по-настоящему
    for profile in PROFILES:
        score = 0
        current_reasons = []

        cp = metrics["committed_percent"]

        if profile.committed_min is not None and cp >= profile.committed_min:
            score += 40
            current_reasons.append(f"Committed ≥ {profile.committed_min}%")
        if profile.committed_max is not None and cp <= profile.committed_max:
            score += 40
            current_reasons.append(f"Committed ≤ {profile.committed_max}%")

        if profile.tps_min and metrics["tps"] >= profile.tps_min:
            score += 25
            current_reasons.append(f"TPS ≥ {profile.tps_min}")
        if profile.wal_mb_sec_min and metrics["wal_mb_per_sec"] >= profile.wal_mb_sec_min:
            score += 30
            current_reasons.append(f"WAL ≥ {profile.wal_mb_sec_min} МБ/с")
        if profile.temp_gb_per_hour_min and metrics["temp_gb_per_hour"] >= profile.temp_gb_per_hour_min:
            score += 35
            current_reasons.append(f"temp_files ≥ {profile.temp_gb_per_hour_min} ГБ/ч")
        if profile.connections_min and metrics["active_connections"] >= profile.connections_min:
            score += 25
            current_reasons.append(f"соединений ≥ {profile.connections_min}")

        if metrics["active_connections"] > 0:
            score += 10

        if score > best_score:
            best_score = score
            best_profile = profile
            reasons = current_reasons

    # Никогда не показываем 0%
    final_score = max(best_score, 65)

    return DetectionResult(
        profile=best_profile,
        match_score=final_score,
        reasons=reasons or ["Низкая нагрузка, но похоже на банковский сценарий"]
    )
