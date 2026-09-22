"""Lifecycle-event constructors.

The functions in this module produce ordinary dictionaries through EventEnvelope.
They do not perform schema validation themselves; callers can validate serialized
payloads through :mod:`batchline.events.validation` when required.
"""

from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from typing import Any, Mapping

from batchline.jobs.models import Job
from batchline.jobs.status import JobStatus
from batchline.config.models import ServiceConfig
from batchline.workers.models import WorkerSnapshot

from .envelope import EventEnvelope

_SEQUENCE = count(1)


def _event_id(prefix: str) -> str:
    return f"{prefix}_{next(_SEQUENCE):06d}"


def _when(value: datetime | None) -> datetime:
    return value or datetime.now(UTC)


def job_event(job: Job, *, occurred_at: datetime | None = None, source: str = "batchline.jobs") -> EventEnvelope:
    event_type_by_status = {
        JobStatus.QUEUED: "job.queued",
        JobStatus.RUNNING: "job.started",
        JobStatus.SUCCEEDED: "job.succeeded",
        JobStatus.FAILED: "job.failed",
        JobStatus.CANCELED: "job.canceled",
    }
    payload: dict[str, Any] = {
        "job_id": job.id,
        "kind": job.kind,
        "queue": job.queue,
        "status": job.status.value,
        "attempt": job.attempt,
        "max_attempts": job.max_attempts,
    }
    if job.result is not None:
        payload["result"] = dict(job.result)
    if job.error is not None:
        payload["error"] = job.error.to_dict()
    return EventEnvelope(
        event_id=_event_id("evt_job"),
        event_type=event_type_by_status[job.status],
        occurred_at=_when(occurred_at),
        source=source,
        payload=payload,
    )


def retry_scheduled_event(
    job: Job,
    *,
    delay_seconds: int,
    occurred_at: datetime | None = None,
    source: str = "batchline.jobs",
) -> EventEnvelope:
    if delay_seconds < 0:
        raise ValueError("delay_seconds cannot be negative")
    return EventEnvelope(
        event_id=_event_id("evt_retry"),
        event_type="job.retry_scheduled",
        occurred_at=_when(occurred_at),
        source=source,
        payload={
            "job_id": job.id,
            "queue": job.queue,
            "attempt": job.attempt,
            "next_attempt": job.attempt + 1,
            "delay_seconds": delay_seconds,
        },
    )


def worker_heartbeat_event(
    snapshot: WorkerSnapshot,
    *,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    return EventEnvelope(
        event_id=_event_id("evt_worker"),
        event_type="worker.heartbeat",
        occurred_at=_when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "active_jobs": snapshot.active_jobs,
            "capacity": snapshot.capacity,
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
        event_id=_event_id("evt_limit"),
        event_type="worker.rate_limited",
        occurred_at=_when(occurred_at),
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
        event_id=_event_id("evt_worker"),
        event_type="worker.unavailable",
        occurred_at=_when(occurred_at),
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
    reason: str,
    occurred_at: datetime | None = None,
    source: str = "batchline.workers",
) -> EventEnvelope:
    if not reason.strip():
        raise ValueError("reason cannot be empty")
    return EventEnvelope(
        event_id=_event_id("evt_worker"),
        event_type="worker.draining",
        occurred_at=_when(occurred_at),
        source=source,
        payload={
            "worker": snapshot.name,
            "service": snapshot.service,
            "queue": snapshot.queue,
            "reason": reason,
            "active_jobs": snapshot.active_jobs,
        },
    )


def service_config_loaded_event(
    config: ServiceConfig,
    *,
    environment: str,
    occurred_at: datetime | None = None,
    source: str = "batchline.config",
) -> EventEnvelope:
    if not environment.strip():
        raise ValueError("environment cannot be empty")
    return EventEnvelope(
        event_id=_event_id("evt_config"),
        event_type="service.config_loaded",
        occurred_at=_when(occurred_at),
        source=source,
        payload={
            "service": config.name,
            "environment": environment,
            "settings": config.settings(),
        },
    )


def service_config_rejected_event(
    service: str,
    *,
    environment: str,
    errors: tuple[str, ...] | list[str],
    occurred_at: datetime | None = None,
    source: str = "batchline.config",
) -> EventEnvelope:
    if not service.strip():
        raise ValueError("service cannot be empty")
    if not environment.strip():
        raise ValueError("environment cannot be empty")
    cleaned = [str(error).strip() for error in errors if str(error).strip()]
    if not cleaned:
        raise ValueError("errors must contain at least one message")
    return EventEnvelope(
        event_id=_event_id("evt_config"),
        event_type="service.config_rejected",
        occurred_at=_when(occurred_at),
        source=source,
        payload={
            "service": service,
            "environment": environment,
            "errors": cleaned,
        },
    )
