"""Detailed offline deployment reporting for Batchline configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .loader import (
    DEFAULT_CONFIG_DIR,
    effective_service_catalog,
    effective_setting_sources,
    load_environment_policy,
)
from .validation import ConfigDiagnostic, validate_deployment


_SETTING_ORDER = ("queue", "concurrency", "timeout_seconds", "max_retries", "enabled")


@dataclass(frozen=True, slots=True)
class DeploymentReport:
    environment: str
    lines: tuple[str, ...]
    diagnostics: tuple[ConfigDiagnostic, ...]

    @property
    def ok(self) -> bool:
        return not self.diagnostics

    def text(self) -> str:
        return "\n".join(self.lines)


def _value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _diagnostics_for_service(
    diagnostics: Iterable[ConfigDiagnostic],
    service: str,
) -> tuple[ConfigDiagnostic, ...]:
    return tuple(item for item in diagnostics if item.service == service)


def build_deployment_report(
    environment: str,
    *,
    config_dir: Path | str = DEFAULT_CONFIG_DIR,
) -> DeploymentReport:
    """Build a deterministic line-oriented report of effective service settings and policy checks."""
    directory = Path(config_dir)
    catalog = effective_service_catalog(environment, config_dir=directory)
    policy = load_environment_policy(environment, config_dir=directory)
    sources = effective_setting_sources(environment, config_dir=directory)
    diagnostics = validate_deployment(environment, config_dir=directory)

    lines: list[str] = [
        f"DEPLOYMENT_REPORT environment={environment} services={len(catalog.services)}",
        f"POLICY default_timeout_seconds={policy.default_timeout_seconds} "
        f"required_services={len(policy.required_settings)} overrides={len(policy.overrides)}",
    ]

    for name in catalog.names():
        config = catalog.get(name)
        settings = config.settings()
        lines.append(f"SERVICE_BEGIN service={name}")
        for key in _SETTING_ORDER:
            lines.append(
                f"SERVICE_SETTING service={name} key={key} value={_value(settings[key])} "
                f"source={sources[name][key]}"
            )

        requirements = policy.required_settings.get(name, {})
        if requirements:
            for key, expected in sorted(requirements.items()):
                actual = settings.get(key)
                status = "ok" if actual == expected else "mismatch"
                lines.append(
                    f"POLICY_CHECK service={name} key={key} expected={_value(expected)} "
                    f"actual={_value(actual)} status={status}"
                )
        else:
            lines.append(f"POLICY_CHECK service={name} status=none")

        service_diagnostics = _diagnostics_for_service(diagnostics, name)
        for diagnostic in service_diagnostics:
            lines.append(f"DIAGNOSTIC {diagnostic.line()}")
        lines.append(
            f"SERVICE_RESULT service={name} status={'ok' if not service_diagnostics else 'failed'}"
        )

    global_diagnostics = tuple(item for item in diagnostics if item.service is None)
    for diagnostic in global_diagnostics:
        lines.append(f"DIAGNOSTIC {diagnostic.line()}")

    lines.append(
        f"DEPLOYMENT_RESULT environment={environment} "
        f"status={'ok' if not diagnostics else 'failed'} errors={len(diagnostics)}"
    )
    return DeploymentReport(environment=environment, lines=tuple(lines), diagnostics=diagnostics)
