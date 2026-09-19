from datetime import UTC, datetime

from batchline.api.serializers.workers import serialize_service_config, serialize_worker_snapshot
from batchline.config.models import ServiceConfig
from batchline.workers.models import WorkerSnapshot


def test_snapshot_serializer_includes_health():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    snapshot = WorkerSnapshot(
        name="thumb-01", service="thumbnailer", queue="media",
        last_seen_at=now, active_jobs=1, capacity=4,
    )
    data = serialize_worker_snapshot(snapshot, now=now)
    assert data["health"] == "healthy"
    assert data["available_slots"] == 3


def test_service_config_serializer_exposes_catalog_values():
    config = ServiceConfig(
        name="thumbnailer",
        queue="media",
        concurrency=4,
        timeout_seconds=120,
        max_retries=4,
    )
    assert serialize_service_config(config) == {
        "name": "thumbnailer",
        "queue": "media",
        "concurrency": 4,
        "timeout_seconds": 120,
        "max_retries": 4,
        "enabled": True,
    }
