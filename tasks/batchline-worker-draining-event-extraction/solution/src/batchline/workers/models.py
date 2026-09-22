"""Runtime worker snapshots."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime


def _parse_time(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


@dataclass(frozen=True, slots=True)
class WorkerSnapshot:
    name: str
    service: str
    queue: str
    last_seen_at: datetime
    active_jobs: int
    capacity: int
    draining: bool = False
    drain_reason: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "last_seen_at", _parse_time(self.last_seen_at))
        for field_name in ("name", "service", "queue"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")
        if self.active_jobs < 0:
            raise ValueError("active_jobs cannot be negative")
        if self.capacity < 1:
            raise ValueError("capacity must be at least 1")
        if self.active_jobs > self.capacity:
            raise ValueError("active_jobs cannot exceed capacity")
        if self.draining:
            if self.drain_reason is None or not self.drain_reason.strip():
                raise ValueError("draining workers require a non-empty drain_reason")
        elif self.drain_reason is not None:
            raise ValueError("non-draining workers cannot retain a drain_reason")

    @property
    def available_slots(self) -> int:
        if self.draining:
            return 0
        return self.capacity - self.active_jobs

    def drain(self, reason: str) -> "WorkerSnapshot":
        cleaned = reason.strip()
        if not cleaned:
            raise ValueError("reason cannot be empty")
        return replace(self, draining=True, drain_reason=cleaned)

    def resume(self) -> "WorkerSnapshot":
        return replace(self, draining=False, drain_reason=None)
