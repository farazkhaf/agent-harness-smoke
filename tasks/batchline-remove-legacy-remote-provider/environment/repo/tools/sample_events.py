#!/usr/bin/env python
"""Print representative events generated through the product encoder."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from batchline.events.encoder import job_event, worker_heartbeat_event
from batchline.jobs.models import Job
from batchline.workers.models import WorkerSnapshot


def main() -> None:
    when = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    job = Job(id="job_demo", kind="thumbnail", queue="media", created_at=when, updated_at=when)
    worker = WorkerSnapshot(
        name="thumb-01",
        service="thumbnailer",
        queue="media",
        last_seen_at=when,
        active_jobs=1,
        capacity=4,
    )
    for event in (job_event(job, occurred_at=when), worker_heartbeat_event(worker, occurred_at=when)):
        print(json.dumps(event.to_dict(), sort_keys=True))


if __name__ == "__main__":
    main()
