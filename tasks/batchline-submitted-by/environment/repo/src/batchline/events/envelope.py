"""Common lifecycle event envelope."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_id: str
    event_type: str
    occurred_at: datetime
    source: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id cannot be empty")
        if not self.event_type.strip():
            raise ValueError("event_type cannot be empty")
        if not self.source.strip():
            raise ValueError("source cannot be empty")
        if self.occurred_at.tzinfo is None:
            object.__setattr__(self, "occurred_at", self.occurred_at.replace(tzinfo=UTC))
        if self.schema_version < 1:
            raise ValueError("schema_version must be positive")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "occurred_at": _iso(self.occurred_at),
            "source": self.source,
            "schema_version": self.schema_version,
            "payload": dict(self.payload),
        }
