import json
from pathlib import Path

import pytest

from batchline.events.validation import EventValidationError, load_event_schema, validate_event


ROOT = Path(__file__).resolve().parents[2]


def test_schema_is_loadable_and_has_rate_limit_event():
    schema = load_event_schema()
    assert "WorkerRateLimitedEvent" in schema["$defs"]


def test_example_event_is_valid():
    event = json.loads((ROOT / "examples/events/job_succeeded.json").read_text())
    validate_event(event)


def test_invalid_status_is_rejected():
    event = json.loads((ROOT / "examples/events/job_succeeded.json").read_text())
    event["payload"]["status"] = "mystery"
    with pytest.raises(EventValidationError):
        validate_event(event)
