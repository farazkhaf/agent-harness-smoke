"""Framework-independent command helpers for workers."""

from __future__ import annotations

from datetime import datetime

from batchline.cli.render.workers import render_worker_table
from batchline.workers.registry import WorkerRegistry


def list_workers(registry: WorkerRegistry, *, queue: str | None = None, now: datetime | None = None) -> str:
    return render_worker_table(registry.list(queue=queue), now=now)


def drain_worker(registry: WorkerRegistry, name: str, reason: str) -> str:
    snapshot = registry.drain(name, reason)
    return f"Draining {snapshot.name}: {snapshot.drain_reason}"


def resume_worker(registry: WorkerRegistry, name: str) -> str:
    snapshot = registry.resume(name)
    return f"Resumed {snapshot.name}"
