"""Fake CodeCarbon-style emissions rows for dashboard demos and tests."""
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from random import choice, randint, uniform
from uuid import UUID, uuid4, uuid7

REGIONS: list[str] = [
    "new south wales",
    "victoria",
    "queensland",
    "western australia",
    "south australia",
    "tasmania",
]

OS_STRINGS: list[str] = [
    "Linux-6.6.114.1-microsoft-standard-WSL2-aarch64-with-glibc2.41",
    "Linux-5.15.0-generic-x86_64-with-glibc2.35",
    "Linux-6.8.0-aws-x86_64-with-glibc2.39",
]

CPU_MODELS: list[str] = [
    "Oryon",
    "AMD EPYC 7763",
    "Intel Xeon Platinum 8275CL",
]

TRACKING_MODES: list[str] = ["process", "machine"]

# NSW grid carbon intensity (kg CO2/kWh)
GRID_INTENSITY_NSW: float = 2.548692


def _random_backdated_timestamp(days_back: int) -> datetime:
    """Random timestamp within the last `days_back` days, timezone-aware UTC."""
    now = datetime.now(tz=timezone.utc)
    delta_seconds = randint(0, days_back * 24 * 60 * 60)
    return now - timedelta(seconds=delta_seconds)


def _build_row(user_id: UUID, days_back: int) -> dict:
    duration = round(uniform(8.0, 28.0), 6)
    cpu_power = round(uniform(0.005, 0.035), 10)
    gpu_power = round(uniform(0.005, 0.035), 10)
    ram_power = 3.0
    cpu_energy = round(cpu_power * duration / 3_600_000, 12)
    gpu_energy = round(gpu_power * duration / 3_600_000, 12)
    ram_energy = round(ram_power * duration / 3_600_000, 12)
    energy_consumed = round(cpu_energy + gpu_energy + ram_energy, 12)

    emissions = round(energy_consumed * GRID_INTENSITY_NSW, 12)
    emissions_rate = round(emissions / duration, 12)

    return {
        "id": uuid7(),
        "timestamp": _random_backdated_timestamp(days_back),
        "run_id": uuid4(),
        "duration": duration,
        "emissions": emissions,
        "emissions_rate": emissions_rate,
        "cpu_power": cpu_power,
        "gpu_power": gpu_power,
        "ram_power": ram_power,
        "cpu_energy": cpu_energy,
        "gpu_energy": gpu_energy,
        "ram_energy": ram_energy,
        "energy_consumed": energy_consumed,
        "water_consumed": 0.0,
        "region": choice(REGIONS),
        "cloud_provider": "",
        "cloud_region": "",
        "os": choice(OS_STRINGS),
        "cpu_count": 10,
        "cpu_model": choice(CPU_MODELS),
        "gpu_count": 0,
        "gpu_model": "Tested with no GPU",
        "longitude": round(uniform(-180.0, 180.0), 6),
        "latitude": round(uniform(-90.0, 90.0), 6),
        "ram_total_size": round(uniform(4.0, 16.0), 6),
        "tracking_mode": choice(TRACKING_MODES),
        "cpu_utilization_percent": round(uniform(55.0, 85.0), 6),
        "gpu_utilization_percent": 0.0,
        "ram_utilization_percent": round(uniform(57.0, 65.0), 6),
        "ram_used_gb": round(uniform(4.0, 8.0), 6),
        "on_cloud": "N",
        "pue": 1.0,
        "wue": 0.0,
        "user_id": user_id,
    }


def build_emission_rows(
    user_ids: Sequence[UUID],
    num_rows: int,
    days_back: int,
) -> list[dict]:
    return [
        _build_row(user_id=choice(user_ids), days_back=days_back)
        for _ in range(num_rows)
    ]
