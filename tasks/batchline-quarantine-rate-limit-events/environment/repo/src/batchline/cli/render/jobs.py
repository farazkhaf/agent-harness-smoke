"""Human-readable job output used by CLI command helpers."""

from __future__ import annotations

from batchline.jobs.models import Job
from batchline.jobs.status import display_label


def render_job_row(job: Job) -> str:
    """Render one compact row suitable for a terminal table."""

    attempt = f"{job.attempt}/{job.max_attempts}"
    return f"{job.id:<14} {display_label(job.status):<10} {job.queue:<12} {attempt:>5}  {job.kind}"


def render_job_detail(job: Job) -> str:
    lines = [
        f"Job: {job.id}",
        f"Kind: {job.kind}",
        f"Queue: {job.queue}",
        f"Status: {display_label(job.status)}",
        f"Attempt: {job.attempt}/{job.max_attempts}",
        f"Created: {job.created_at.isoformat()}",
        f"Updated: {job.updated_at.isoformat()}",
    ]
    if job.result is not None:
        lines.append(f"Result keys: {', '.join(sorted(job.result)) or '-'}")
    if job.error is not None:
        lines.extend([f"Error: {job.error.code}", f"Message: {job.error.message}"])
    return "\n".join(lines)


def render_job_table(jobs: tuple[Job, ...] | list[Job]) -> str:
    header = f"{'JOB':<14} {'STATUS':<10} {'QUEUE':<12} {'TRY':>5}  KIND"
    rule = "-" * len(header)
    rows = [render_job_row(job) for job in jobs]
    return "\n".join([header, rule, *rows])
