"""Shared execution-provider request, plan, and validation primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shlex
from typing import Mapping, Protocol


@dataclass(frozen=True)
class ExecutionRequest:
    job_id: str
    kind: str
    queue: str
    command: tuple[str, ...]
    working_directory: str = "/app"
    environment: Mapping[str, str] = field(default_factory=dict)
    timeout_seconds: int = 300
    max_output_kb: int = 1024
    trace_id: str | None = None

    def validate(self) -> None:
        if not self.job_id.strip():
            raise ValueError("job_id cannot be empty")
        if not self.kind.strip():
            raise ValueError("kind cannot be empty")
        if not self.queue.strip():
            raise ValueError("queue cannot be empty")
        if not self.command:
            raise ValueError("command cannot be empty")
        if self.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be positive")
        if self.max_output_kb < 1:
            raise ValueError("max_output_kb must be positive")


@dataclass(frozen=True)
class ExecutionPlan:
    provider: str
    argv: tuple[str, ...]
    cwd: str
    environment: Mapping[str, str]
    timeout_seconds: int
    max_output_kb: int
    labels: Mapping[str, str] = field(default_factory=dict)

    def shell_command(self) -> str:
        return " ".join(shlex.quote(part) for part in self.argv)


class ExecutionProvider(Protocol):
    name: str

    def plan(self, request: ExecutionRequest) -> ExecutionPlan:
        ...


def _clean_environment(values: Mapping[str, str]) -> dict[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in values.items():
        name = str(key).strip()
        if not name or "=" in name or "\x00" in name:
            raise ValueError(f"invalid environment variable name: {key!r}")
        text = str(value)
        if "\x00" in text:
            raise ValueError(f"environment variable {name} contains a NUL byte")
        cleaned[name] = text
    return cleaned


def _base_labels(request: ExecutionRequest) -> dict[str, str]:
    labels = {
        "batchline.job_id": request.job_id,
        "batchline.kind": request.kind,
        "batchline.queue": request.queue,
    }
    if request.trace_id:
        labels["batchline.trace_id"] = request.trace_id
    return labels


def _safe_working_directory(value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        raise ValueError("working_directory must be absolute")
    return str(path)


