#!/usr/bin/env python
"""Generate a deterministic Batchline JSONL operational archive."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
from pathlib import Path

from batchline.operations import ArchiveRecord, write_archive

WORKERS = tuple(f"worker-{index:02d}" for index in range(1, 17))
SERVICES = ("thumbnailer", "transcoder", "notifier", "billing", "indexer")
QUEUES = ("media", "notifications", "billing", "search")
PROVIDERS = ("images-api", "video-api", "smtp", "payments-api")
EVENT_TYPES = (
    "worker.heartbeat",
    "job.started",
    "job.succeeded",
    "worker.rate_limited",
    "job.failed",
)


def records(count: int):
    start = datetime(2026, 8, 14, 0, 0, tzinfo=UTC)
    for index in range(count):
        worker = WORKERS[index % len(WORKERS)]
        service = SERVICES[(index * 3) % len(SERVICES)]
        queue = QUEUES[(index * 5) % len(QUEUES)]
        event_type = EVENT_TYPES[(index * 7) % len(EVENT_TYPES)]
        provider = PROVIDERS[(index * 11) % len(PROVIDERS)] if event_type == "worker.rate_limited" else None
        occurred = start + timedelta(seconds=index * 3)
        yield ArchiveRecord(
            event_id=f"arc-{index:07d}",
            occurred_at=occurred.isoformat().replace("+00:00", "Z"),
            event_type=event_type,
            worker=worker,
            service=service,
            queue=queue,
            provider=provider,
            job_id=f"job-{(index * 13) % 10000:05d}",
            detail={"sequence": index, "bucket": index % 9},
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--count", type=int, default=18000)
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be positive")
    write_archive(args.path, records(args.count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
