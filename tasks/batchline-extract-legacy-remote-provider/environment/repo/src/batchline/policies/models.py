"""Typed policy models for configured job kinds."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class JobPolicy:
    kind: str
    owner: str
    queue: str
    enabled: bool
    priority: str
    worker_pool: str
    concurrency_class: str
    retry_policy: str
    max_attempts: int
    timeout_seconds: int
    max_runtime_seconds: int
    lease_seconds: int
    heartbeat_grace_seconds: int
    visibility_timeout_seconds: int
    rate_limit_class: str
    backoff_policy: str
    dead_letter_queue: str
    payload_limit_kb: int
    result_ttl_seconds: int
    idempotency_window_seconds: int
    dedupe_window_seconds: int
    trace_sample_rate: float
    emit_started_event: bool
    emit_progress_event: bool
    retain_failure_payload: bool
    audit_level: str

    @classmethod
    def from_mapping(cls, kind: str, data: Mapping[str, Any]) -> "JobPolicy":
        required = {
            "owner",
            "queue",
            "enabled",
            "priority",
            "worker_pool",
            "concurrency_class",
            "retry_policy",
            "max_attempts",
            "timeout_seconds",
            "max_runtime_seconds",
            "lease_seconds",
            "heartbeat_grace_seconds",
            "visibility_timeout_seconds",
            "rate_limit_class",
            "backoff_policy",
            "dead_letter_queue",
            "payload_limit_kb",
            "result_ttl_seconds",
            "idempotency_window_seconds",
            "dedupe_window_seconds",
            "trace_sample_rate",
            "emit_started_event",
            "emit_progress_event",
            "retain_failure_payload",
            "audit_level",
        }
        unknown = set(data) - required
        missing = required - set(data)
        if unknown:
            raise ValueError(f"unknown policy settings for {kind}: {', '.join(sorted(unknown))}")
        if missing:
            raise ValueError(f"missing policy settings for {kind}: {', '.join(sorted(missing))}")

        policy = cls(
            kind=kind,
            owner=str(data["owner"]),
            queue=str(data["queue"]),
            enabled=bool(data["enabled"]),
            priority=str(data["priority"]),
            worker_pool=str(data["worker_pool"]),
            concurrency_class=str(data["concurrency_class"]),
            retry_policy=str(data["retry_policy"]),
            max_attempts=int(data["max_attempts"]),
            timeout_seconds=int(data["timeout_seconds"]),
            max_runtime_seconds=int(data["max_runtime_seconds"]),
            lease_seconds=int(data["lease_seconds"]),
            heartbeat_grace_seconds=int(data["heartbeat_grace_seconds"]),
            visibility_timeout_seconds=int(data["visibility_timeout_seconds"]),
            rate_limit_class=str(data["rate_limit_class"]),
            backoff_policy=str(data["backoff_policy"]),
            dead_letter_queue=str(data["dead_letter_queue"]),
            payload_limit_kb=int(data["payload_limit_kb"]),
            result_ttl_seconds=int(data["result_ttl_seconds"]),
            idempotency_window_seconds=int(data["idempotency_window_seconds"]),
            dedupe_window_seconds=int(data["dedupe_window_seconds"]),
            trace_sample_rate=float(data["trace_sample_rate"]),
            emit_started_event=bool(data["emit_started_event"]),
            emit_progress_event=bool(data["emit_progress_event"]),
            retain_failure_payload=bool(data["retain_failure_payload"]),
            audit_level=str(data["audit_level"]),
        )
        policy.validate()
        return policy

    def validate(self) -> None:
        if not self.kind.strip():
            raise ValueError("job policy kind cannot be empty")
        if not self.owner.strip() or not self.queue.strip() or not self.worker_pool.strip():
            raise ValueError(f"job policy {self.kind} requires owner, queue, and worker_pool")
        if self.priority not in {"low", "normal", "high", "critical"}:
            raise ValueError(f"unsupported priority for {self.kind}: {self.priority}")
        if self.retry_policy not in {"none", "standard", "aggressive"}:
            raise ValueError(f"unsupported retry_policy for {self.kind}: {self.retry_policy}")
        if self.max_attempts < 1:
            raise ValueError(f"max_attempts must be positive for {self.kind}")
        for name, value in {
            "timeout_seconds": self.timeout_seconds,
            "max_runtime_seconds": self.max_runtime_seconds,
            "lease_seconds": self.lease_seconds,
            "heartbeat_grace_seconds": self.heartbeat_grace_seconds,
            "visibility_timeout_seconds": self.visibility_timeout_seconds,
            "payload_limit_kb": self.payload_limit_kb,
            "result_ttl_seconds": self.result_ttl_seconds,
            "idempotency_window_seconds": self.idempotency_window_seconds,
            "dedupe_window_seconds": self.dedupe_window_seconds,
        }.items():
            if value < 0:
                raise ValueError(f"{name} cannot be negative for {self.kind}")
        if not 0 <= self.trace_sample_rate <= 1:
            raise ValueError(f"trace_sample_rate must be between 0 and 1 for {self.kind}")


class JobPolicyCatalog:
    def __init__(self, policies: Mapping[str, JobPolicy]):
        self._policies = dict(policies)

    def get(self, kind: str) -> JobPolicy:
        try:
            return self._policies[kind]
        except KeyError as exc:
            raise KeyError(f"unknown job policy: {kind}") from exc

    def kinds(self) -> tuple[str, ...]:
        return tuple(sorted(self._policies))

    def __len__(self) -> int:
        return len(self._policies)
