"""Worker heartbeat health classification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from .models import WorkerSnapshot


class WorkerHealth(StrEnum):
    HEALTHY = "healthy"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class HealthPolicy:
    stale_after_seconds: int = 60
    unavailable_after_seconds: int = 180

    def __post_init__(self) -> None:
        if self.stale_after_seconds < 1:
            raise ValueError("stale_after_seconds must be positive")
        if self.unavailable_after_seconds <= self.stale_after_seconds:
            raise ValueError("unavailable threshold must exceed stale threshold")

    def classify(self, snapshot: WorkerSnapshot, *, now: datetime | None = None) -> WorkerHealth:
        reference = now or datetime.now(UTC)
        age = reference - snapshot.last_seen_at
        if age >= timedelta(seconds=self.unavailable_after_seconds):
            return WorkerHealth.UNAVAILABLE
        if age >= timedelta(seconds=self.stale_after_seconds):
            return WorkerHealth.STALE
        return WorkerHealth.HEALTHY
