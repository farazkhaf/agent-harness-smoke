"""Public dictionary representations for job API consumers."""

from __future__ import annotations

from typing import Any

from batchline.jobs.models import Job
from batchline.jobs.status import display_label, is_terminal, status_category


def _iso(value) -> str:
    return value.isoformat().replace("+00:00", "Z")


def serialize_job(job: Job, *, include_payload: bool = False) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": job.id,
        "kind": job.kind,
        "queue": job.queue,
        "status": job.status.value,
        "attempt": job.attempt,
        "max_attempts": job.max_attempts,
        "created_at": _iso(job.created_at),
        "updated_at": _iso(job.updated_at),
    }
    if include_payload:
        data["payload"] = dict(job.payload)
    if job.result is not None:
        data["result"] = dict(job.result)
    if job.error is not None:
        data["error"] = job.error.to_dict()
    return data


def serialize_job_summary(job: Job) -> dict[str, Any]:
    return {
        "id": job.id,
        "kind": job.kind,
        "queue": job.queue,
        "status": job.status.value,
        "status_label": display_label(job.status),
        "status_category": status_category(job.status),
        "terminal": is_terminal(job.status),
    }


def serialize_job_collection(jobs: list[Job] | tuple[Job, ...]) -> dict[str, Any]:
    return {"items": [serialize_job_summary(job) for job in jobs], "count": len(jobs)}
