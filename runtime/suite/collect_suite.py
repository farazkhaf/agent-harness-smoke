#!/usr/bin/env python3
"""Aggregate normalized trial reports for one harness-evaluation suite."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUNTIME / "report"))

from suite_config import load_suite  # noqa: E402
from report_trial import flat_row  # noqa: E402

SCHEMA_VERSION = "0.1"


def load_reports(root: Path) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for path in root.rglob("report.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("schema_version") != "0.3" or data.get("suite") != "coding-harness-smoke":
            continue
        data["_report_path"] = str(path)
        reports.append(data)
    return reports


def enrich(report: dict[str, Any], suite: dict[str, Any]) -> dict[str, Any]:
    task_map = {t["id"]: t for t in suite["tasks"]}
    task = task_map.get(report["task"]["id"], {})
    row = flat_row(report)
    report_path = Path(report.get("_report_path", ""))
    attempt = None
    for part in report_path.parts:
        if part.startswith("attempt-"):
            try:
                attempt = int(part.split("-", 1)[1])
            except ValueError:
                pass
    row.update({
        "attempt": attempt,
        "task_version": task.get("version"),
        "family": task.get("family"),
        "primitive": task.get("primitive"),
    })
    return row


def median_or_none(values: list[Any]) -> Any:
    nums = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return median(nums) if nums else None


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = (row["task"], row["harness"], row["harness_version"], row["provider"], row["model"])
        grouped[key].append(row)
    out: list[dict[str, Any]] = []
    for key, group in grouped.items():
        task, harness, harness_version, provider, model = key
        out.append({
            "task": task,
            "harness": harness,
            "harness_version": harness_version,
            "provider": provider,
            "model": model,
            "runs": len(group),
            "passes": sum(1 for r in group if r["passed"]),
            "pass_rate": sum(1 for r in group if r["passed"]) / len(group),
            "median_reward": median_or_none([r["reward"] for r in group]),
            "median_inference_calls": median_or_none([r["inference_calls"] for r in group]),
            "median_input_tokens": median_or_none([r["input_tokens"] for r in group]),
            "median_cached_tokens": median_or_none([r["cached_tokens"] for r in group]),
            "median_output_tokens": median_or_none([r["output_tokens"] for r in group]),
            "median_cost_usd": median_or_none([r["cost_usd"] for r in group]),
            "median_total_seconds": median_or_none([r["total_seconds"] for r in group]),
        })
    return sorted(out, key=lambda r: (str(r["task"]), str(r["harness"])))


def scenario_group_summary(value: Any) -> str:
    if not isinstance(value, dict):
        return "—"
    parts = []
    for name, detail in sorted(value.items()):
        if isinstance(detail, dict):
            status = detail.get("status", "?")
        else:
            status = detail
        parts.append(f"{name}={status}")
    return ", ".join(parts) if parts else "—"


def reward_groups(value: Any) -> str:
    if not isinstance(value, dict):
        return "—"
    items = [(k, v) for k, v in value.items() if k != "reward"]
    if not items:
        return "—"
    return ", ".join(f"{k}={v}" for k, v in sorted(items))


def md_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        if abs(value) < 1 and value != 0:
            return f"{value:.4f}"
        return f"{value:.2f}"
    return str(value)


def markdown(suite: dict[str, Any], rows: list[dict[str, Any]], summary: list[dict[str, Any]]) -> str:
    lines = [
        f"# {suite['id']} results",
        "",
        suite.get("description", ""),
        "",
        "> Compact suite report only. Raw Harbor/native trajectories remain separate drill-down artifacts and are not interpreted here. Calls/tokens/cost/time are descriptive route/resource telemetry; smaller wall time is not treated as inherently better.",
        "",
        "## Runs",
        "",
        "| Task | Harness | Attempt | Reward | Verifier groups | Calls | Input | Cached | Output | Cost USD | Total s |",
        "|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['task']}` | `{r['harness']}` | {md_value(r.get('attempt'))} | {md_value(r['reward'])} | {scenario_group_summary(r.get('verifier_groups')) if r.get('verifier_groups') else reward_groups(r.get('verifier_rewards'))} | {md_value(r['inference_calls'])} | "
            f"{md_value(r['input_tokens'])} | {md_value(r['cached_tokens'])} | {md_value(r['output_tokens'])} | "
            f"{md_value(r['cost_usd'])} | {md_value(r['total_seconds'])} |"
        )
    if not rows:
        lines.append("| — | — | — | — | — | — | — | — | — | — | — |")

    if any(s["runs"] > 1 for s in summary):
        lines += [
            "",
            "## Repeated-run aggregates",
            "",
            "| Task | Harness | Runs | Pass rate | Median reward | Median calls | Median input | Median output | Median cost |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for s in summary:
            lines.append(
                f"| `{s['task']}` | `{s['harness']}` | {s['runs']} | {s['pass_rate']:.2f} | "
                f"{md_value(s['median_reward'])} | {md_value(s['median_inference_calls'])} | "
                f"{md_value(s['median_input_tokens'])} | {md_value(s['median_output_tokens'])} | {md_value(s['median_cost_usd'])} |"
            )
    return "\n".join(lines) + "\n"


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "task", "task_version", "family", "primitive", "attempt", "harness", "harness_version", "provider", "model",
        "trial", "passed", "reward", "verifier_rewards", "verifier_groups",
        "workspace_changed_files", "workspace_lines_added", "workspace_lines_deleted", "workspace_untracked_files",
        "workspace_changed_files_total", "workspace_untracked_text_lines_added",
        "workspace_text_lines_added_total", "workspace_text_lines_deleted_total",
        "inference_calls", "input_tokens", "cached_tokens", "uncached_input_tokens",
        "output_tokens", "cost_usd", "total_seconds", "agent_execution_seconds",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        csv_rows = []
        for row in rows:
            item = dict(row)
            item["verifier_rewards"] = json.dumps(item.get("verifier_rewards") or {}, ensure_ascii=False, sort_keys=True)
            item["verifier_groups"] = json.dumps(item.get("verifier_groups") or {}, ensure_ascii=False, sort_keys=True)
            csv_rows.append(item)
        writer.writerows(csv_rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate normalized reports for a harness-evaluation suite")
    ap.add_argument("--suite", type=Path, required=True)
    ap.add_argument("--reports-root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    suite = load_suite(args.suite.resolve())
    task_ids = {t["id"] for t in suite["tasks"]}
    reports = [r for r in load_reports(args.reports_root.resolve()) if r.get("task", {}).get("id") in task_ids]
    rows = [enrich(r, suite) for r in reports]
    rows.sort(key=lambda r: (
        str(r["task"]),
        str(r["harness"]),
        r["attempt"] if isinstance(r.get("attempt"), int) else 10**9,
        str(r["trial"]),
    ))
    summary = aggregate(rows)

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "suite": {k: suite.get(k) for k in ("id", "kind", "description", "repeats")},
        "runs": rows,
        "aggregates": summary,
    }
    (out / "results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(rows, out / "results.csv")
    (out / "results.md").write_text(markdown(suite, rows, summary), encoding="utf-8")
    print(f"Collected {len(rows)} run(s) into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
