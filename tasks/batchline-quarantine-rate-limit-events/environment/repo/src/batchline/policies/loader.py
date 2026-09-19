"""Load the TOML job-policy catalog shipped with Batchline."""

from __future__ import annotations

from pathlib import Path
import tomllib
from typing import Any

from .models import JobPolicy, JobPolicyCatalog

DEFAULT_POLICY_PATH = Path(__file__).resolve().parents[3] / "config" / "job-policies.toml"


def load_job_policies(path: Path | str = DEFAULT_POLICY_PATH) -> JobPolicyCatalog:
    policy_path = Path(path)
    document: dict[str, Any] = tomllib.loads(policy_path.read_text(encoding="utf-8"))
    raw = document.get("jobs")
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{policy_path} must contain a non-empty [jobs] catalog")
    policies: dict[str, JobPolicy] = {}
    for kind, data in raw.items():
        if not isinstance(data, dict):
            raise ValueError(f"job policy {kind} must be a table")
        policies[str(kind)] = JobPolicy.from_mapping(str(kind), data)
    return JobPolicyCatalog(policies)
