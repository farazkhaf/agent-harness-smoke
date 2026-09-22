"""YAML configuration loading, schema validation, and environment overlay."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml

from .models import EnvironmentPolicy, ServiceCatalog, ServiceConfig
from .schema import validate_service_document


DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


def _read_yaml(path: Path) -> Mapping[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def load_service_document(path: Path | str = DEFAULT_CONFIG_DIR / "services.yaml") -> Mapping[str, Any]:
    document = _read_yaml(Path(path))
    validate_service_document(document)
    return document


def load_service_catalog(path: Path | str = DEFAULT_CONFIG_DIR / "services.yaml") -> ServiceCatalog:
    document = load_service_document(path)
    raw_services = document["services"]

    services: dict[str, ServiceConfig] = {}
    for name, raw in raw_services.items():
        services[name] = ServiceConfig.from_mapping(str(name), raw)
    return ServiceCatalog(services)


def load_environment_policy(
    environment: str,
    *,
    config_dir: Path | str = DEFAULT_CONFIG_DIR,
) -> EnvironmentPolicy:
    directory = Path(config_dir)
    path = directory / "environments" / f"{environment}.yaml"
    document = _read_yaml(path)
    if document.get("name") != environment:
        raise ValueError(f"environment file {path} must declare name: {environment}")
    return EnvironmentPolicy(
        name=environment,
        default_timeout_seconds=int(document.get("default_timeout_seconds", 60)),
        required_settings=document.get("required_settings", {}) or {},
        overrides=document.get("overrides", {}) or {},
    )


def effective_service_catalog(
    environment: str,
    *,
    config_dir: Path | str = DEFAULT_CONFIG_DIR,
) -> ServiceCatalog:
    directory = Path(config_dir)
    base = load_service_catalog(directory / "services.yaml")
    policy = load_environment_policy(environment, config_dir=directory)
    unknown_override_services = set(policy.overrides) - set(base.services)
    if unknown_override_services:
        names = ", ".join(sorted(unknown_override_services))
        raise ValueError(f"environment overrides unknown services: {names}")

    merged: dict[str, ServiceConfig] = {}
    for name, config in base.services.items():
        values = config.settings()
        overrides = policy.overrides.get(name, {})
        unknown_keys = set(overrides) - set(values)
        if unknown_keys:
            keys = ", ".join(sorted(unknown_keys))
            raise ValueError(f"environment overrides unknown settings for {name}: {keys}")
        values.update(overrides)
        merged[name] = ServiceConfig.from_mapping(name, values)
    return ServiceCatalog(merged)


def effective_setting_sources(
    environment: str,
    *,
    config_dir: Path | str = DEFAULT_CONFIG_DIR,
) -> Mapping[str, Mapping[str, str]]:
    """Return whether each effective setting came from base config or an environment override."""
    directory = Path(config_dir)
    base = load_service_catalog(directory / "services.yaml")
    policy = load_environment_policy(environment, config_dir=directory)
    sources: dict[str, dict[str, str]] = {}
    for name, config in base.services.items():
        service_sources = {key: "base" for key in config.settings()}
        for key in policy.overrides.get(name, {}):
            if key in service_sources:
                service_sources[key] = "override"
        sources[name] = service_sources
    return sources
