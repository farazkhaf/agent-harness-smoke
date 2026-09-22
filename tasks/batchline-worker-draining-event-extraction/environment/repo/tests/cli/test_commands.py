from datetime import UTC, datetime

from batchline.cli.commands.jobs import cancel_job, list_jobs, show_job
from batchline.cli.commands.workers import list_workers
from batchline.jobs.models import Job
from batchline.jobs.service import JobService
from batchline.workers.models import WorkerSnapshot
from batchline.workers.registry import WorkerRegistry


def test_job_command_helpers_use_domain_service():
    when = datetime(2026, 1, 1, tzinfo=UTC)
    service = JobService([
        Job(id="job-1", kind="thumbnail", queue="media", created_at=when, updated_at=when),
        Job(id="job-2", kind="notify", queue="notifications", created_at=when, updated_at=when),
    ])
    assert "job-1" in list_jobs(service, queue="media")
    assert "job-2" not in list_jobs(service, queue="media")
    assert "thumbnail" in show_job(service, "job-1")
    assert cancel_job(service, "job-1") == "Canceled job-1"


def test_worker_command_helper_renders_registry():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    registry = WorkerRegistry([
        WorkerSnapshot(
            name="thumb-01",
            service="thumbnailer",
            queue="media",
            last_seen_at=now,
            active_jobs=1,
            capacity=4,
        )
    ])
    output = list_workers(registry, queue="media", now=now)
    assert "thumb-01" in output
    assert "healthy" in output
