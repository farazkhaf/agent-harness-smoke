from datetime import UTC, datetime

from batchline.cli.render.workers import render_worker_row
from batchline.workers.models import WorkerSnapshot


def test_worker_row_contains_health_and_load():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    snapshot = WorkerSnapshot(
        name="thumb-01", service="thumbnailer", queue="media",
        last_seen_at=now, active_jobs=1, capacity=4,
    )
    row = render_worker_row(snapshot, now=now)
    assert "healthy" in row
    assert "1/4" in row
