from pathlib import Path

from batchline.config.reporting import build_deployment_report


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"


def test_production_report_is_detailed_and_stable():
    report = build_deployment_report("production", config_dir=CONFIG)
    assert report.ok
    assert len(report.lines) >= 80
    assert report.lines[0] == "DEPLOYMENT_REPORT environment=production services=10"
    assert "SERVICE_BEGIN service=thumbnailer" in report.lines
    assert (
        "SERVICE_SETTING service=thumbnailer key=max_retries value=4 source=base"
        in report.lines
    )
    assert (
        "POLICY_CHECK service=thumbnailer key=max_retries expected=4 actual=4 status=ok"
        in report.lines
    )
    assert report.lines[-1] == "DEPLOYMENT_RESULT environment=production status=ok errors=0"


def test_development_report_marks_overrides():
    report = build_deployment_report("development", config_dir=CONFIG)
    assert report.ok
    assert (
        "SERVICE_SETTING service=thumbnailer key=concurrency value=1 source=override"
        in report.lines
    )
    assert (
        "SERVICE_SETTING service=archiver key=enabled value=false source=override"
        in report.lines
    )


def test_report_surfaces_policy_mismatch(tmp_path):
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
    report = build_deployment_report("production", config_dir=config)
    assert not report.ok
    assert any(
        line == "POLICY_CHECK service=thumbnailer key=max_retries expected=4 actual=2 status=mismatch"
        for line in report.lines
    )
    assert any("DIAGNOSTIC CONFIG_MISMATCH service=thumbnailer" in line for line in report.lines)
    assert report.lines[-1] == "DEPLOYMENT_RESULT environment=production status=failed errors=1"
