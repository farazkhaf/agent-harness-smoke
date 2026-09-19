"""Runtime worker snapshots."""

from __future__ import annotations

from dataclasses import dataclass
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

    @property
    def available_slots(self) -> int:
        return self.capacity - self.active_jobs
