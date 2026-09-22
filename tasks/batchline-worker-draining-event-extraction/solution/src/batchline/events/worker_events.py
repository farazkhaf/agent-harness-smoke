"""Worker lifecycle-event constructors."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from batchline.workers.models import WorkerSnapshot

from ._common import event_id, when
from .envelope import EventEnvelope


def worker_heartbeat_event(
    snapshot: WorkerSnapshot,
    *,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id("evt_worker"),
        event_type="worker.heartbeat",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "active_jobs": snapshot.active_jobs,
            "capacity": snapshot.capacity,
            "draining": snapshot.draining,
        },
    )


def worker_rate_limited_event(
    snapshot: WorkerSnapshot,
    *,
    provider: str,
    limit_name: str,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
    detail: Mapping[str, Any] | None = None,
) -> EventEnvelope:
    payload: dict[str, Any] = {
        "worker": snapshot.name,
        "service": snapshot.service,
        "queue": snapshot.queue,
        "provider": provider,
        "limit_name": limit_name,
    }
    if detail:
        payload["detail"] = dict(detail)
    return EventEnvelope(
        event_id=event_id("evt_limit"),
        event_type="worker.rate_limited",
        occurred_at=when(occurred_at),
        source=source,
        payload=payload,
    )


def worker_unavailable_event(
    snapshot: WorkerSnapshot,
    *,
    unavailable_seconds: int,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    if unavailable_seconds < 1:
        raise ValueError("unavailable_seconds must be positive")
    return EventEnvelope(
        event_id=event_id("evt_worker"),
        event_type="worker.unavailable",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "last_seen_at": snapshot.last_seen_at.isoformat().replace("+00:00", "Z"),
            "unavailable_seconds": unavailable_seconds,
        },
    )


def worker_draining_event(
    snapshot: WorkerSnapshot,
    *,
    reason: str | None = None,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    if reason is None:
        if not snapshot.draining or snapshot.drain_reason is None:
            raise ValueError("a non-draining snapshot requires an explicit reason")
        resolved_reason = snapshot.drain_reason
    else:
        resolved_reason = reason.strip()
        if not resolved_reason:
            raise ValueError("reason cannot be empty")
        if snapshot.draining and snapshot.drain_reason != resolved_reason:
            raise ValueError("explicit reason does not match snapshot drain_reason")
    return EventEnvelope(
        event_id=event_id("evt_worker"),
        event_type="worker.draining",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "reason": resolved_reason,
            "active_jobs": snapshot.active_jobs,
        },
    )


def worker_resumed_event(
    snapshot: WorkerSnapshot,
    *,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    if snapshot.draining:
        raise ValueError("worker.resumed requires a non-draining snapshot")
    return EventEnvelope(
        event_id=event_id("evt_worker"),
        event_type="worker.resumed",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "active_jobs": snapshot.active_jobs,
            "capacity": snapshot.capacity,
        },
    )
