from datetime import UTC, datetime

from batchline.workers.models import WorkerSnapshot
from batchline.workers.registry import WorkerRegistry


def snapshot(name, queue, active, capacity):
    return WorkerSnapshot(
        name=name,
        service=name.split("-")[0],
        queue=queue,
        last_seen_at=datetime(2026, 1, 1, tzinfo=UTC),
        active_jobs=active,
        capacity=capacity,
    )


def test_registry_filters_and_counts_capacity():
    registry = WorkerRegistry([
        snapshot("thumb-01", "media", 1, 4),
        snapshot("thumb-02", "media", 3, 4),
        snapshot("notify-01", "notifications", 1, 8),
    ])
    assert len(registry.list(queue="media")) == 2
    assert registry.total_available_slots(queue="media") == 4
