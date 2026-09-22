from pathlib import Path

from batchline.config.loader import (
    effective_service_catalog,
    effective_setting_sources,
    load_environment_policy,
    load_service_catalog,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"


def test_load_service_catalog():
    catalog = load_service_catalog(CONFIG / "services.yaml")
    assert set(catalog.services) == {
        "archiver",
        "auditor",
        "cleanup",
        "exporter",
        "importer",
        "indexer",
        "notifier",
        "reconciler",
        "thumbnailer",
        "webhook",
    }
    assert catalog.get("thumbnailer").max_retries == 4
    assert catalog.get("thumbnailer").name == "thumbnailer"
    assert catalog.total_concurrency == 40


def test_development_overrides_concurrency():
    catalog = effective_service_catalog("development", config_dir=CONFIG)
    assert catalog.get("thumbnailer").concurrency == 1
    assert catalog.get("thumbnailer").max_retries == 4
    assert catalog.get("archiver").enabled is False


def test_setting_sources_identify_environment_overrides():
    sources = effective_setting_sources("development", config_dir=CONFIG)
    assert sources["thumbnailer"]["concurrency"] == "override"
    assert sources["thumbnailer"]["max_retries"] == "base"
    assert sources["archiver"]["enabled"] == "override"


def test_production_policy_has_requirements():
    policy = load_environment_policy("production", config_dir=CONFIG)
    assert policy.required_settings["thumbnailer"]["max_retries"] == 4
    assert policy.required_settings["webhook"]["timeout_seconds"] == 30


def test_unknown_override_setting_is_rejected(tmp_path):
    config = tmp_path / "config"
    (config / "environments").mkdir(parents=True)
    (config / "services.yaml").write_text(
        """services:
  thumbnailer:
    queue: media
    concurrency: 4
    timeout_seconds: 120
    max_retries: 4
    enabled: true
"""
    )
    (config / "environments" / "development.yaml").write_text(
        """name: development
default_timeout_seconds: 120
required_settings: {}
overrides:
  thumbnailer:
    unknown_setting: true
"""
    )
    import pytest

    with pytest.raises(ValueError, match="unknown settings"):
        effective_service_catalog("development", config_dir=config)
