"""Streaming helpers for line-oriented Batchline operational archives."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Any


@dataclass(frozen=True)
class ArchiveRecord:
    event_id: str
    occurred_at: str
    event_type: str
    worker: str
    service: str
    queue: str
    provider: str | None = None
    job_id: str | None = None
    detail: Mapping[str, Any] | None = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ArchiveRecord":
        return cls(
            event_id=str(data["event_id"]),
            occurred_at=str(data["occurred_at"]),
            event_type=str(data["event_type"]),
            worker=str(data["worker"]),
            service=str(data["service"]),
            queue=str(data["queue"]),
            provider=None if data.get("provider") is None else str(data["provider"]),
            job_id=None if data.get("job_id") is None else str(data["job_id"]),
            detail=data.get("detail"),
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "event_id": self.event_id,
            "occurred_at": self.occurred_at,
            "event_type": self.event_type,
            "worker": self.worker,
            "service": self.service,
            "queue": self.queue,
        }
        if self.provider is not None:
            data["provider"] = self.provider
        if self.job_id is not None:
            data["job_id"] = self.job_id
        if self.detail is not None:
            data["detail"] = dict(self.detail)
        return data


def iter_archive(path: Path | str) -> Iterator[ArchiveRecord]:
    archive_path = Path(path)
    with archive_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at line {line_number}: {exc.msg}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"archive line {line_number} must contain a JSON object")
            yield ArchiveRecord.from_mapping(payload)


def write_archive(path: Path | str, records: Iterable[ArchiveRecord]) -> None:
    archive_path = Path(path)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with archive_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def matching_event_ids(
    path: Path | str,
    *,
    worker: str,
    event_type: str,
    provider: str | None = None,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
) -> tuple[str, ...]:
    matches: list[tuple[str, str]] = []
    for record in iter_archive(path):
        if record.worker != worker or record.event_type != event_type:
            continue
        if provider is not None and record.provider != provider:
            continue
        occurred = datetime.fromisoformat(record.occurred_at.replace("Z", "+00:00"))
        if start_at is not None and occurred < start_at:
            continue
        if end_at is not None and occurred > end_at:
            continue
        matches.append((record.occurred_at, record.event_id))
    matches.sort()
    return tuple(event_id for _, event_id in matches)
