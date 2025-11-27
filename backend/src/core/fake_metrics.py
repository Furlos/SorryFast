# core/fake_metrics.py
from faker import Faker
from random import uniform, randint

fake = Faker("ru_RU")  # чтобы было по-русски, если надо

def generate_fake_metrics(profile_name: str):
    rules = {
        "Classic OLTP": {"committed": (70, 95), "tps": (500, 3000), "wal": (50, 150), "temp": (0, 2)},
        "Financial-Safe OLTP": {"committed": (90, 99), "tps": (300, 1500), "wal": (80, 200), "temp": (0, 0.5)},
        "Analytical OLAP": {"committed": (5, 30), "tps": (10, 200), "wal": (5, 50), "temp": (30, 200)},
        "Write-heavy IoT & Telemetry": {"committed": (60, 85), "tps": (5000, 50000), "wal": (200, 800), "temp": (0, 10)},
        "High-Concurrency Web/API": {"committed": (75, 95), "tps": (2000, 8000), "wal": (40, 120), "temp": (0, 3)},
        "Batch/ETL & Night Loads": {"committed": (5, 25), "tps": (50, 500), "wal": (200, 600), "temp": (100, 500)},
        "Mixed OLTP + Periodic Analytics": {"committed": (40, 70), "tps": (800, 4000), "wal": (60, 180), "temp": (5, 40)},
        "Read-Heavy / In-Memory Cache": {"committed": (5, 20), "tps": (100, 800), "wal": (10, 60), "temp": (0, 5)},
    }

    r = rules.get(profile_name, rules["Classic OLTP"])

    return {
        "tps": round(uniform(*r["tps"]), 1),
        "wal_mb_per_sec": round(uniform(*r["wal"]), 1),
        "temp_gb_per_hour": round(uniform(*r["temp"]), 1),
        "committed_percent": round(uniform(*r["committed"]), 1),
        "active_connections": randint(10, 8000),
        "top_wait_event": fake.random_element([
            "CPU",
            "IO: DataFileRead",
            "IO: DataFileWrite",
            "Lock: transactionid",
            "Client: ClientRead"
        ])
    }