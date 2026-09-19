from datetime import UTC, datetime

import pytest

from batchline.jobs.models import Job


@pytest.fixture
def fixed_time():
    return datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


@pytest.fixture
def queued_job(fixed_time):
    return Job(
        id="job_123",
        kind="thumbnail",
        queue="media",
        max_attempts=4,
        created_at=fixed_time,
        updated_at=fixed_time,
        payload={"asset_id": "asset_42"},
    )
