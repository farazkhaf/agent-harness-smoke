from datetime import UTC, datetime, timedelta

from batchline.workers.health import HealthPolicy, WorkerHealth
from batchline.workers.models import WorkerSnapshot


def make_snapshot(last_seen):
    return WorkerSnapshot(
        name="thumb-01",
        service="thumbnailer",
        queue="media",
        last_seen_at=last_seen,
        active_jobs=1,
        capacity=4,
    )


def test_health_thresholds():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    policy = HealthPolicy(stale_after_seconds=60, unavailable_after_seconds=180)
    assert policy.classify(make_snapshot(now - timedelta(seconds=20)), now=now) is WorkerHealth.HEALTHY
    assert policy.classify(make_snapshot(now - timedelta(seconds=90)), now=now) is WorkerHealth.STALE
    assert policy.classify(make_snapshot(now - timedelta(seconds=240)), now=now) is WorkerHealth.UNAVAILABLE
