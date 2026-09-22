"""Framework-independent command helpers for jobs."""

from __future__ import annotations

from batchline.jobs.service import JobService
from batchline.jobs.status import parse_status_filter
from batchline.cli.render.jobs import render_job_detail, render_job_table


def list_jobs(service: JobService, *, statuses: tuple[str, ...] = (), queue: str | None = None) -> str:
    if not statuses:
        jobs = service.list(queue=queue)
    else:
        selected = set(parse_status_filter(statuses))
        jobs = tuple(job for job in service.list(queue=queue) if job.status in selected)
    return render_job_table(jobs)


def show_job(service: JobService, job_id: str) -> str:
    return render_job_detail(service.get(job_id))


def cancel_job(service: JobService, job_id: str) -> str:
    job = service.cancel(job_id)
    return f"Canceled {job.id}"
