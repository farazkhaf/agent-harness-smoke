from datetime import UTC, datetime

from batchline.config.models import ServiceConfig
from batchline.events.encoder import (
    job_event,
    service_config_loaded_event,
    service_config_rejected_event,
    worker_draining_event,
    worker_heartbeat_event,
    worker_rate_limited_event,
    worker_unavailable_event,
)
from batchline.events.validation import validate_event
from batchline.workers.models import WorkerSnapshot


def _worker(fixed_time):
    return WorkerSnapshot(
        name="thumb-01",
        service="thumbnailer",
        queue="media",
        last_seen_at=fixed_time,
        active_jobs=1,
        capacity=4,
    )


def test_job_event_matches_schema(queued_job, fixed_time):
    event = job_event(queued_job, occurred_at=fixed_time).to_dict()
    assert event["event_type"] == "job.queued"
    assert event["payload"]["status"] == "queued"
    validate_event(event)


def test_worker_events_match_schema(fixed_time):
    snapshot = _worker(fixed_time)
    events = [
        worker_heartbeat_event(snapshot, occurred_at=fixed_time),
        worker_rate_limited_event(
            snapshot,
            provider="images-api",
            limit_name="requests-per-minute",
            occurred_at=fixed_time,
            detail={"bucket": "standard"},
        ),
        worker_unavailable_event(snapshot, unavailable_seconds=240, occurred_at=fixed_time),
        worker_draining_event(snapshot, reason="rolling-restart", occurred_at=fixed_time),
    ]
    for event in events:
        validate_event(event.to_dict())


def test_service_config_events_match_schema(fixed_time):
    config = ServiceConfig(
        name="thumbnailer",
        queue="media",
        concurrency=4,
        timeout_seconds=120,
        max_retries=4,
        enabled=True,
    )
    loaded = service_config_loaded_event(
        config,
        environment="production",
        occurred_at=fixed_time,
    ).to_dict()
    rejected = service_config_rejected_event(
        "thumbnailer",
        environment="production",
        errors=["max_retries did not satisfy production policy"],
        occurred_at=fixed_time,
    ).to_dict()
    validate_event(loaded)
    validate_event(rejected)
    assert loaded["payload"]["settings"]["max_retries"] == 4
    assert rejected["payload"]["errors"]
