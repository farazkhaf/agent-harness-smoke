from pathlib import Path

import pytest

from batchline.config.loader import load_service_catalog
from batchline.config.schema import ServiceConfigSchemaError
from batchline.config.validation import validate_deployment


ROOT = Path(__file__).resolve().parents[2]


def test_production_configuration_is_valid():
    assert validate_deployment("production", config_dir=ROOT / "config") == ()


def test_mismatch_reports_stable_fields(tmp_path):
    config = tmp_path / "config"
    (config / "environments").mkdir(parents=True)
    (config / "services.yaml").write_text(
        """services:
  thumbnailer:
    queue: media
    concurrency: 4
    timeout_seconds: 120
    max_retries: 2
    enabled: true
"""
    )
    (config / "environments" / "production.yaml").write_text(
        """name: production
default_timeout_seconds: 60
required_settings:
  thumbnailer:
    max_retries: 4
overrides: {}
"""
    )
    diagnostics = validate_deployment("production", config_dir=config)
    assert len(diagnostics) == 1
    line = diagnostics[0].line()
    assert "CONFIG_MISMATCH" in line
    assert "service=thumbnailer" in line
    assert "key=max_retries" in line
    assert "expected=4" in line
    assert "actual=2" in line


def test_raw_catalog_is_schema_validated(tmp_path):
    path = tmp_path / "services.yaml"
    path.write_text(
        """services:
  thumbnailer:
    queue: media
    concurrency: 0
    timeout_seconds: 120
    max_retries: 4
    enabled: true
"""
    )
    with pytest.raises(ServiceConfigSchemaError, match="concurrency"):
        load_service_catalog(path)
