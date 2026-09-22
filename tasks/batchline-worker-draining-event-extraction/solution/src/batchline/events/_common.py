"""Shared support for lifecycle-event constructors."""

from __future__ import annotations

from datetime import UTC, datetime
from itertools import count

_SEQUENCE = count(1)


def event_id(prefix: str) -> str:
    return f"{prefix}_{next(_SEQUENCE):06d}"


def when(value: datetime | None) -> datetime:
    return value or datetime.now(UTC)
