"""Lifecycle-event constructors.

The functions in this module produce ordinary dictionaries through EventEnvelope.
They do not perform schema validation themselves; callers can validate serialized
payloads through :mod:`batchline.events.validation` when required.

Worker event constructors are implemented in :mod:`batchline.events.worker_events`
and re-exported here for compatibility with existing imports.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from batchline.jobs.models import Job
from batchline.jobs.status import JobStatus
from batchline.config.models import ServiceConfig

from ._common import event_id, when
from .envelope import EventEnvelope
from .worker_events import (
    worker_draining_event,
    worker_heartbeat_event,
    worker_rate_limited_event,
    worker_resumed_event,
    worker_unavailable_event,
)


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
        event_id=event_id("evt_job"),
        event_type=event_type_by_status[job.status],
        occurred_at=when(occurred_at),
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
        event_id=event_id("evt_retry"),
        event_type="job.retry_scheduled",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "job_id": job.id,
            "queue": job.queue,
            "attempt": job.attempt,
            "next_attempt": job.attempt + 1,
            "delay_seconds": delay_seconds,
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
        event_id=event_id("evt_config"),
        event_type="service.config_loaded",
        occurred_at=when(occurred_at),
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
        event_id=event_id("evt_config"),
        event_type="service.config_rejected",
        occurred_at=when(occurred_at),
        source=source,
        payload={
            "service": service,
            "environment": environment,
            "errors": cleaned,
        },
    )
