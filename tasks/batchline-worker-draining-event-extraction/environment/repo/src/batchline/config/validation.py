"""Deployment-oriented configuration checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .loader import DEFAULT_CONFIG_DIR, effective_service_catalog, load_environment_policy


@dataclass(frozen=True, slots=True)
class ConfigDiagnostic:
    code: str
    service: str | None
    key: str | None
    message: str
    expected: Any = None
    actual: Any = None

    def line(self) -> str:
        parts = [self.code]
        if self.service is not None:
            parts.append(f"service={self.service}")
        if self.key is not None:
            parts.append(f"key={self.key}")
        if self.expected is not None:
            parts.append(f"expected={self.expected}")
        if self.actual is not None:
            parts.append(f"actual={self.actual}")
        parts.append(f"message={self.message}")
        return " ".join(parts)


def validate_deployment(
    environment: str,
    *,
    config_dir: Path | str = DEFAULT_CONFIG_DIR,
) -> tuple[ConfigDiagnostic, ...]:
    directory = Path(config_dir)
    catalog = effective_service_catalog(environment, config_dir=directory)
    policy = load_environment_policy(environment, config_dir=directory)
    diagnostics: list[ConfigDiagnostic] = []

    for service_name, requirements in policy.required_settings.items():
        if service_name not in catalog.services:
            diagnostics.append(
                ConfigDiagnostic(
                    code="CONFIG_MISSING_SERVICE",
                    service=service_name,
                    key=None,
                    message="required service is not declared",
                )
            )
            continue

        config = catalog.services[service_name]
        values = config.to_dict()
        for key, expected in requirements.items():
            actual = values.get(key)
            if actual != expected:
                diagnostics.append(
                    ConfigDiagnostic(
                        code="CONFIG_MISMATCH",
                        service=service_name,
                        key=key,
                        expected=expected,
                        actual=actual,
                        message="effective deployment setting does not match environment policy",
                    )
                )

    for name, config in catalog.services.items():
        if environment == "production" and not config.enabled:
            diagnostics.append(
                ConfigDiagnostic(
                    code="CONFIG_DISABLED_SERVICE",
                    service=name,
                    key="enabled",
                    expected=True,
                    actual=False,
                    message="production service is disabled",
                )
            )
        if config.timeout_seconds > 900:
            diagnostics.append(
                ConfigDiagnostic(
                    code="CONFIG_TIMEOUT_HIGH",
                    service=name,
                    key="timeout_seconds",
                    expected="<=900",
                    actual=config.timeout_seconds,
                    message="service timeout exceeds deployment limit",
                )
            )

    return tuple(diagnostics)
