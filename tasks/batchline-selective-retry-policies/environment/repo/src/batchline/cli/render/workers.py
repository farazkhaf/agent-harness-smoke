"""Human-readable worker output."""

from __future__ import annotations

from datetime import datetime

from batchline.workers.health import HealthPolicy
from batchline.workers.models import WorkerSnapshot


def render_worker_row(
    snapshot: WorkerSnapshot,
    *,
    policy: HealthPolicy | None = None,
    now: datetime | None = None,
) -> str:
    health = (policy or HealthPolicy()).classify(snapshot, now=now).value
    slots = f"{snapshot.active_jobs}/{snapshot.capacity}"
    return f"{snapshot.name:<18} {health:<11} {snapshot.queue:<12} {slots:>5}"


def render_worker_table(snapshots: tuple[WorkerSnapshot, ...], *, now: datetime | None = None) -> str:
    header = f"{'WORKER':<18} {'HEALTH':<11} {'QUEUE':<12} {'LOAD':>5}"
    rule = "-" * len(header)
    rows = [render_worker_row(snapshot, now=now) for snapshot in snapshots]
    return "\n".join([header, rule, *rows])
