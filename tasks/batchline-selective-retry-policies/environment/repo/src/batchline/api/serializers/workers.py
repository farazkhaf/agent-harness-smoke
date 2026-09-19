"""Public worker and service representations."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from batchline.config.models import ServiceConfig
from batchline.workers.health import HealthPolicy
from batchline.workers.models import WorkerSnapshot


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def serialize_service_config(config: ServiceConfig) -> dict[str, Any]:
    return config.to_dict()


def serialize_worker_snapshot(
    snapshot: WorkerSnapshot,
    *,
    policy: HealthPolicy | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    health_policy = policy or HealthPolicy()
    return {
        "name": snapshot.name,
        "service": snapshot.service,
        "queue": snapshot.queue,
        "last_seen_at": _iso(snapshot.last_seen_at),
        "active_jobs": snapshot.active_jobs,
        "capacity": snapshot.capacity,
        "available_slots": snapshot.available_slots,
        "health": health_policy.classify(snapshot, now=now).value,
    }
