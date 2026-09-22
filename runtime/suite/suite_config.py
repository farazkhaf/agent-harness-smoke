#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
from typing import Any

SUPPORTED_SCHEMA_VERSIONS = {"0.1", "0.2"}
SUPPORTED_EXECUTION_MODES = {"preinstalled", "external"}
SUPPORTED_SUITE_KINDS = {"focused-task", "scenario"}


def _validate_profile(profile: dict[str, Any]) -> None:
    profile_id = profile.get("id")
    if not profile_id:
        raise ValueError("Every suite profile must declare a non-empty id")

    mode = profile.get("execution", "preinstalled")
    if mode not in SUPPORTED_EXECUTION_MODES:
        raise ValueError(f"Unsupported execution mode for profile {profile_id!r}: {mode!r}")

    if mode == "preinstalled":
        if not profile.get("runtime_profile"):
            raise ValueError(f"Preinstalled profile {profile_id!r} requires runtime_profile")
        if not profile.get("model"):
            raise ValueError(f"Preinstalled profile {profile_id!r} requires model")
    else:
        if not profile.get("agent"):
            raise ValueError(f"External profile {profile_id!r} requires agent import path")
        # External/custom agents may own model/provider configuration themselves.
        # `model` therefore remains optional rather than being fabricated.


def load_suite(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        data = tomllib.load(f)
    schema_version = data.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(f"Unsupported suite schema: {schema_version!r}")
    if data.get("kind") not in SUPPORTED_SUITE_KINDS:
        raise ValueError(f"Unsupported suite kind: {data.get('kind')!r}")
    tasks = data.get("tasks") or []
    profiles = data.get("profiles") or []
    if not tasks or not profiles:
        raise ValueError("Suite must declare at least one task and one profile")
    ids = [t.get("id") for t in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("Task ids must be unique")
    profile_ids = [p.get("id") for p in profiles]
    if len(profile_ids) != len(set(profile_ids)):
        raise ValueError("Profile ids must be unique")
    for profile in profiles:
        _validate_profile(profile)
    repeats = int(data.get("repeats", 1))
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    data["repeats"] = repeats
    return data


def execution_plan(suite: dict[str, Any]) -> list[dict[str, Any]]:
    plan: list[dict[str, Any]] = []
    for task in suite["tasks"]:
        for profile in suite["profiles"]:
            mode = profile.get("execution", "preinstalled")
            for attempt in range(1, suite["repeats"] + 1):
                plan.append({
                    "task_id": task["id"],
                    "task_version": task.get("version"),
                    "task_path": task["path"],
                    "family": task.get("family"),
                    "primitive": task.get("primitive"),
                    "profile_id": profile["id"],
                    "execution": mode,
                    "runtime_profile": profile.get("runtime_profile"),
                    "agent": profile.get("agent"),
                    "model": profile.get("model"),
                    "attempt": attempt,
                })
    return plan


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite", type=Path)
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args()
    suite = load_suite(args.suite.resolve())
    payload = execution_plan(suite) if args.plan else suite
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
