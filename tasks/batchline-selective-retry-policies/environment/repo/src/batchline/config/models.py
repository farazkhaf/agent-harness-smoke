"""Typed deployment configuration objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ServiceConfig:
    """Effective configuration for one Batchline service."""

    name: str
    queue: str
    concurrency: int
    timeout_seconds: int
    max_retries: int
    enabled: bool = True

    def __post_init__(self) -> None:
        for field_name in ("name", "queue"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")
        if self.concurrency < 1:
            raise ValueError("concurrency must be at least 1")
        if self.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be at least 1")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")

    @classmethod
    def from_mapping(cls, name: str, data: Mapping[str, Any]) -> "ServiceConfig":
        return cls(
            name=name,
            queue=str(data["queue"]),
            concurrency=int(data["concurrency"]),
            timeout_seconds=int(data["timeout_seconds"]),
            max_retries=int(data["max_retries"]),
            enabled=bool(data.get("enabled", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "queue": self.queue,
            "concurrency": self.concurrency,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "enabled": self.enabled,
        }

    def settings(self) -> dict[str, Any]:
        """Return configurable fields without the catalog key/name."""
        data = self.to_dict()
        data.pop("name")
        return data


@dataclass(frozen=True, slots=True)
class ServiceCatalog:
    services: Mapping[str, ServiceConfig]

    def __post_init__(self) -> None:
        if not self.services:
            raise ValueError("service catalog cannot be empty")
        for name, config in self.services.items():
            if name != config.name:
                raise ValueError(f"service key {name!r} does not match config name {config.name!r}")

    def get(self, name: str) -> ServiceConfig:
        try:
            return self.services[name]
        except KeyError:
            raise KeyError(f"unknown service: {name}") from None

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self.services))

    def for_queue(self, queue: str) -> tuple[ServiceConfig, ...]:
        return tuple(
            config
            for _, config in sorted(self.services.items())
            if config.queue == queue
        )

    @property
    def total_concurrency(self) -> int:
        return sum(config.concurrency for config in self.services.values() if config.enabled)


@dataclass(frozen=True, slots=True)
class EnvironmentPolicy:
    name: str
    default_timeout_seconds: int
    required_settings: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)
    overrides: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("environment name cannot be empty")
        if self.default_timeout_seconds < 1:
            raise ValueError("default_timeout_seconds must be positive")
        unknown_sections = set(self.required_settings) | set(self.overrides)
        if any(not str(name).strip() for name in unknown_sections):
            raise ValueError("service names in environment policy cannot be empty")
