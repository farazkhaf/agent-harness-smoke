"""In-memory registry for worker snapshots."""

from __future__ import annotations

from collections.abc import Iterable

from .models import WorkerSnapshot


class WorkerRegistry:
    def __init__(self, snapshots: Iterable[WorkerSnapshot] = ()) -> None:
        self._snapshots = {snapshot.name: snapshot for snapshot in snapshots}

    def update(self, snapshot: WorkerSnapshot) -> None:
        self._snapshots[snapshot.name] = snapshot

    def get(self, name: str) -> WorkerSnapshot:
        try:
            return self._snapshots[name]
        except KeyError:
            raise KeyError(f"unknown worker: {name}") from None

    def remove(self, name: str) -> None:
        self._snapshots.pop(name, None)

    def list(self, *, service: str | None = None, queue: str | None = None) -> tuple[WorkerSnapshot, ...]:
        items = self._snapshots.values()
        if service is not None:
            items = (item for item in items if item.service == service)
        if queue is not None:
            items = (item for item in items if item.queue == queue)
        return tuple(sorted(items, key=lambda item: item.name))

    def total_available_slots(self, *, queue: str | None = None) -> int:
        return sum(snapshot.available_slots for snapshot in self.list(queue=queue))
