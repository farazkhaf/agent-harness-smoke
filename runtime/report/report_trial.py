#!/usr/bin/env python3
"""Normalize one Harbor trial into a compact architecture-neutral report.

Schema 0.3 deliberately keeps the normal report surface small. Harbor
``result.json`` is authoritative for outcome, verifier rewards, timings and
normalized token/cost totals. A generic inference-call count may be accepted
from Harbor agent metadata, a harness-provided ``smoke_telemetry.json`` sidecar,
or Harbor's normalized ATIF trajectory. No native harness trajectory parsing,
private reasoning extraction, tool-mix analysis, or edit-strategy inference is
part of the public report path.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

SCHEMA_VERSION = "0.3"
SUITE = "coding-harness-smoke"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def duration_seconds(block: Optional[dict[str, Any]]) -> Optional[float]:
    if not block:
        return None
    start = parse_dt(block.get("started_at"))
    end = parse_dt(block.get("finished_at"))
    if not start or not end:
        return None
    return round((end - start).total_seconds(), 6)


def total_duration(result: dict[str, Any]) -> Optional[float]:
    start = parse_dt(result.get("started_at"))
    end = parse_dt(result.get("finished_at"))
    if not start or not end:
        return None
    return round((end - start).total_seconds(), 6)


def first_existing(root: Path, names: list[str]) -> Optional[Path]:
    if not root.exists():
        return None
    for name in names:
        direct = root / name
        if direct.exists():
            return direct
    for p in root.rglob("*"):
        if p.is_file() and p.name in names:
            return p
    return None


def _numeric(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    return None


def inference_calls_from_mapping(data: Any) -> Optional[int]:
    if not isinstance(data, dict):
        return None
    for key in ("inference_calls", "model_calls", "llm_calls", "api_calls"):
        value = _numeric(data.get(key))
        if value is not None:
            return value
    return None


def inference_calls_from_atif(path: Path) -> Optional[int]:
    """Read only normalized call-count fields from ATIF, never reasoning/tools."""
    try:
        data = load_json(path)
    except Exception:
        return None

    final_metrics = data.get("final_metrics") or {}
    direct = inference_calls_from_mapping(final_metrics)
    if direct is not None:
        return direct

    total = 0
    saw = False
    for step in data.get("steps") or []:
        value = _numeric((step or {}).get("llm_call_count"))
        if value is not None:
            saw = True
            total += value
    return total if saw else None


def generic_inference_calls(trial_dir: Path, agent_result: dict[str, Any]) -> tuple[Optional[int], Optional[str]]:
    """Resolve architecture-neutral inference count with explicit provenance."""
    metadata = agent_result.get("metadata") or {}
    value = inference_calls_from_mapping(metadata)
    if value is not None:
        return value, "harbor_agent_metadata"

    sidecar = first_existing(trial_dir, ["smoke_telemetry.json"])
    if sidecar is not None:
        try:
            value = inference_calls_from_mapping(load_json(sidecar))
        except Exception:
            value = None
        if value is not None:
            return value, "smoke_telemetry"

    atif = first_existing(trial_dir / "agent", ["trajectory.json"])
    if atif is not None:
        value = inference_calls_from_atif(atif)
        if value is not None:
            return value, "harbor_atif"

    return None, None


def normalize_trial(trial_dir: Path) -> dict[str, Any]:
    result_path = trial_dir / "result.json"
    if not result_path.exists():
        raise FileNotFoundError(f"No result.json found in {trial_dir}")
    result = load_json(result_path)

    agent_info = result.get("agent_info") or {}
    model_info = agent_info.get("model_info") or {}
    agent_result = result.get("agent_result") or {}
    verifier_result = result.get("verifier_result") or {}
    rewards = verifier_result.get("rewards") or {}
    reward = rewards.get("reward")

    config = result.get("config") or {}
    agent_cfg = config.get("agent") or {}
    task_cfg = config.get("task") or {}

    task_id = result.get("task_name") or result.get("task_id") or task_cfg.get("name") or task_cfg.get("path")
    if isinstance(task_id, dict):
        task_id = task_id.get("path") or task_id.get("name") or str(task_id)

    harness_name = agent_info.get("name") or agent_cfg.get("name") or agent_cfg.get("import_path")
    harbor_agent = agent_cfg.get("import_path") or agent_cfg.get("name") or harness_name

    raw_input_tokens = agent_result.get("n_input_tokens")
    cached_tokens = agent_result.get("n_cache_tokens")
    uncached_input_tokens = None
    if isinstance(raw_input_tokens, (int, float)) and isinstance(cached_tokens, (int, float)):
        if raw_input_tokens >= cached_tokens:
            uncached_input_tokens = raw_input_tokens - cached_tokens

    inference_calls, inference_source = generic_inference_calls(trial_dir, agent_result)

    verifier_groups = None
    group_artifact = first_existing(trial_dir, ["scenario_verifier_groups.json"])
    if group_artifact is not None:
        try:
            group_payload = load_json(group_artifact)
            if isinstance(group_payload, dict):
                verifier_groups = group_payload.get("groups")
        except Exception:
            verifier_groups = None

    workspace_observation = None
    observation_artifact = first_existing(
        trial_dir,
        ["scenario_workspace_observation.json", "smoke_observation.json"],
    )
    if observation_artifact is not None:
        try:
            candidate = load_json(observation_artifact)
            if isinstance(candidate, dict):
                workspace_observation = candidate
        except Exception:
            workspace_observation = None

    return {
        "schema_version": SCHEMA_VERSION,
        "suite": SUITE,
        "trial": {
            "id": result.get("id"),
            "name": result.get("trial_name"),
            "task_checksum": result.get("task_checksum"),
        },
        "task": {
            "id": task_id,
        },
        "agent": {
            "harness": harness_name,
            "harness_version": agent_info.get("version"),
            "harbor_agent": harbor_agent,
            "provider": model_info.get("provider"),
            "model": model_info.get("name") or agent_cfg.get("model_name"),
        },
        "outcome": {
            "passed": bool(reward is not None and float(reward) > 0),
            "reward": reward,
            "rewards": rewards,
            "exception": result.get("exception_info"),
        },
        "timing": {
            "total_seconds": total_duration(result),
            "environment_setup_seconds": duration_seconds(result.get("environment_setup")),
            "agent_setup_seconds": duration_seconds(result.get("agent_setup")),
            "agent_execution_seconds": duration_seconds(result.get("agent_execution")),
            "verifier_seconds": duration_seconds(result.get("verifier")),
        },
        "telemetry": {
            "inference_calls": inference_calls,
            "inference_calls_source": inference_source,
            "input_tokens": raw_input_tokens,
            "cached_tokens": cached_tokens,
            "uncached_input_tokens": uncached_input_tokens,
            "output_tokens": agent_result.get("n_output_tokens"),
            "cost_usd": agent_result.get("cost_usd"),
        },
        "diagnostics": {
            "verifier_groups": verifier_groups,
            "workspace_observation": workspace_observation,
        },
        "notes": {
            "report_boundary": "Compact public/quick-look report. Raw Harbor/native trajectories remain separate drill-down evidence.",
            "telemetry_semantics": "input_tokens is Harbor's full prompt/context total when available; cached_tokens is a subset. inference_calls is optional and architecture-neutral; missing means unavailable, not zero.",
            "task_checksum_semantics": "Group cross-harness comparisons by logical task id, not runtime-bound Harbor checksum alone.",
        },
    }


def fmt(v: Any) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)


def markdown(report: dict[str, Any]) -> str:
    a = report["agent"]
    o = report["outcome"]
    t = report["timing"]
    m = report["telemetry"]
    model = f"{a.get('provider')}/{a.get('model')}" if a.get("provider") else a.get("model")
    lines = [
        "# Harness Smoke Trial Report",
        "",
        f"- **Trial:** `{report['trial']['name']}`",
        f"- **Task:** `{report['task']['id']}`",
        f"- **Harness:** `{a['harness']}`" + (f" `{a['harness_version']}`" if a.get("harness_version") else ""),
        f"- **Model:** `{model}`",
        f"- **Outcome:** {'PASS' if o['passed'] else 'FAIL'} (reward={fmt(o['reward'])})",
        "",
        "## Quick metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Inference/model calls | {fmt(m['inference_calls'])} |",
        f"| Input tokens | {fmt(m['input_tokens'])} |",
        f"| Cached input tokens | {fmt(m['cached_tokens'])} |",
        f"| Derived uncached input tokens | {fmt(m['uncached_input_tokens'])} |",
        f"| Output tokens | {fmt(m['output_tokens'])} |",
        f"| Cost (USD) | {fmt(m['cost_usd'])} |",
        f"| Total seconds | {fmt(t['total_seconds'])} |",
        f"| Agent execution seconds | {fmt(t['agent_execution_seconds'])} |",
        "",
        "## Verifier rewards",
        "",
        "```json",
        json.dumps(o["rewards"], indent=2, ensure_ascii=False),
        "```",
    ]
    diagnostics = report.get("diagnostics") or {}
    groups = diagnostics.get("verifier_groups")
    observation = diagnostics.get("workspace_observation")
    if groups is not None:
        lines += [
            "",
            "## Scenario verifier groups",
            "",
            "```json",
            json.dumps(groups, indent=2, ensure_ascii=False),
            "```",
        ]
    if isinstance(observation, dict):
        lines += [
            "",
            "## Workspace observation",
            "",
            f"- Tracked changed files: {fmt(observation.get('changed_files'))}",
            f"- Tracked lines added/deleted: {fmt(observation.get('lines_added'))} / {fmt(observation.get('lines_deleted'))}",
            f"- Untracked files: {fmt(observation.get('untracked_files'))}",
        ]
        if observation.get("workspace_changed_files_total") is not None:
            lines += [
                f"- Total observed changed files: {fmt(observation.get('workspace_changed_files_total'))}",
                f"- Untracked text lines added: {fmt(observation.get('untracked_text_lines_added'))}",
                f"- Total observed text lines added/deleted: {fmt(observation.get('workspace_text_lines_added_total'))} / {fmt(observation.get('workspace_text_lines_deleted_total'))}",
            ]
    lines += [
        "",
        "> Raw trajectories are intentionally not summarized here. They remain available as drill-down evidence in the Harbor trial artifacts.",
    ]
    return "\n".join(lines) + "\n"


def flat_row(report: dict[str, Any]) -> dict[str, Any]:
    t = report["timing"]
    m = report["telemetry"]
    diagnostics = report.get("diagnostics") or {}
    observation = diagnostics.get("workspace_observation") or {}
    return {
        "trial": report["trial"]["name"],
        "task": report["task"]["id"],
        "harness": report["agent"]["harness"],
        "harness_version": report["agent"]["harness_version"],
        "provider": report["agent"]["provider"],
        "model": report["agent"]["model"],
        "passed": report["outcome"]["passed"],
        "reward": report["outcome"]["reward"],
        "verifier_rewards": report["outcome"]["rewards"],
        "verifier_groups": diagnostics.get("verifier_groups"),
        "workspace_changed_files": observation.get("changed_files"),
        "workspace_lines_added": observation.get("lines_added"),
        "workspace_lines_deleted": observation.get("lines_deleted"),
        "workspace_untracked_files": observation.get("untracked_files"),
        "workspace_changed_files_total": observation.get("workspace_changed_files_total"),
        "workspace_untracked_text_lines_added": observation.get("untracked_text_lines_added"),
        "workspace_text_lines_added_total": observation.get("workspace_text_lines_added_total"),
        "workspace_text_lines_deleted_total": observation.get("workspace_text_lines_deleted_total"),
        "inference_calls": m["inference_calls"],
        "input_tokens": m["input_tokens"],
        "cached_tokens": m["cached_tokens"],
        "uncached_input_tokens": m["uncached_input_tokens"],
        "output_tokens": m["output_tokens"],
        "cost_usd": m["cost_usd"],
        "total_seconds": t["total_seconds"],
        "agent_execution_seconds": t["agent_execution_seconds"],
    }


def write_csv(report: dict[str, Any], path: Path) -> None:
    row = flat_row(report)
    row["verifier_rewards"] = json.dumps(row["verifier_rewards"], ensure_ascii=False, sort_keys=True)
    row["verifier_groups"] = json.dumps(row.get("verifier_groups") or {}, ensure_ascii=False, sort_keys=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def write_report(report: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "report.md").write_text(markdown(report), encoding="utf-8")
    write_csv(report, out / "summary.csv")


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize a Harbor trial into compact smoke report artifacts")
    ap.add_argument("trial_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None, help="Output directory (default: <trial>/smoke-report)")
    args = ap.parse_args()

    trial_dir = args.trial_dir.resolve()
    out = (args.out or (trial_dir / "smoke-report")).resolve()
    report = normalize_trial(trial_dir)
    write_report(report, out)
    print(f"Wrote {out / 'report.json'}")
    print(f"Wrote {out / 'report.md'}")
    print(f"Wrote {out / 'summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
