import json
from pathlib import Path

import pytest

from batchline.events.validation import EventValidationError, WORKER_SCHEMA, load_event_schema, validate_event


ROOT = Path(__file__).resolve().parents[2]


def test_event_schemas_are_loadable_and_worker_definitions_are_split():
    schema = load_event_schema()
    worker_schema = load_event_schema(WORKER_SCHEMA)
    assert "WorkerRateLimitedEvent" not in schema["$defs"]
    assert "WorkerRateLimitedEvent" in worker_schema["$defs"]


def test_example_event_is_valid():
    event = json.loads((ROOT / "examples/events/job_succeeded.json").read_text())
    validate_event(event)


def test_invalid_status_is_rejected():
    event = json.loads((ROOT / "examples/events/job_succeeded.json").read_text())
    event["payload"]["status"] = "mystery"
    with pytest.raises(EventValidationError):
        validate_event(event)
