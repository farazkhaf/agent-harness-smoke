"""Registry of supported event types and their product domains."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventTypeInfo:
    name: str
    domain: str
    description: str


_EVENT_TYPES: tuple[EventTypeInfo, ...] = (
    EventTypeInfo("job.queued", "job", "A job was accepted into a queue."),
    EventTypeInfo("job.started", "job", "A worker began executing a job."),
    EventTypeInfo("job.succeeded", "job", "A job completed successfully."),
    EventTypeInfo("job.failed", "job", "A job attempt failed."),
    EventTypeInfo("job.canceled", "job", "A job was canceled before completion."),
    EventTypeInfo("job.retry_scheduled", "job", "A failed job was scheduled for another attempt."),
    EventTypeInfo("worker.heartbeat", "worker", "A worker reported liveness and capacity."),
    EventTypeInfo("worker.unavailable", "worker", "A worker exceeded the liveness threshold."),
    EventTypeInfo("worker.rate_limited", "worker", "A worker reported upstream rate limiting."),
    EventTypeInfo("worker.draining", "worker", "A worker stopped accepting new work."),
    EventTypeInfo("worker.resumed", "worker", "A worker resumed accepting new work."),
    EventTypeInfo("service.config_loaded", "service", "A service configuration was loaded."),
    EventTypeInfo("service.config_rejected", "service", "A service configuration failed validation."),
)

_BY_NAME = {item.name: item for item in _EVENT_TYPES}


def event_type_info(name: str) -> EventTypeInfo:
    try:
        return _BY_NAME[name]
    except KeyError:
        raise KeyError(f"unsupported event type: {name}") from None


def event_types(*, domain: str | None = None) -> tuple[EventTypeInfo, ...]:
    if domain is None:
        return _EVENT_TYPES
    return tuple(item for item in _EVENT_TYPES if item.domain == domain)


def is_supported_event_type(name: str) -> bool:
    return name in _BY_NAME
