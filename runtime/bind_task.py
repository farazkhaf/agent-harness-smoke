#!/usr/bin/env python3
"""Materialize a temporary Harbor task bound to a preinstalled agent image.

Canonical task content stays agent-agnostic. The only binding operation is to
replace the default HARNESS_SMOKE_BASE_IMAGE in environment/Dockerfile with the
image declared by a runtime profile. Repository setup logic remains canonical
and is not rewritten here.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

BASE_ARG_RE = re.compile(r"^ARG\s+HARNESS_SMOKE_BASE_IMAGE\s*=\s*(?P<value>\S+)\s*$")


def _read_profile_scalar(profile: Path, key: str) -> str:
    """Read a top-level scalar from the simple runtime-profile YAML format.

    Runtime profiles deliberately keep the binding keys as top-level scalars,
    so the binder does not need a YAML dependency of its own.
    """

    prefix = f"{key}:"
    for raw in profile.read_text(encoding="utf-8").splitlines():
        if raw.startswith((" ", "\t", "#")) or not raw.strip():
            continue
        if raw.startswith(prefix):
            value = raw[len(prefix) :].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            if not value:
                raise ValueError(f"runtime profile key {key!r} is empty: {profile}")
            return value
    raise ValueError(f"runtime profile is missing top-level key {key!r}: {profile}")


def bind_task(task: Path, profile: Path, output: Path, *, force: bool = False) -> dict[str, str]:
    task = task.resolve()
    profile = profile.resolve()
    output = output.resolve()

    if not (task / "task.toml").is_file():
        raise ValueError(f"not a Harbor task (task.toml missing): {task}")
    dockerfile = task / "environment" / "Dockerfile"
    if not dockerfile.is_file():
        raise ValueError(f"canonical task environment/Dockerfile missing: {dockerfile}")
    if not profile.is_file():
        raise ValueError(f"runtime profile missing: {profile}")

    profile_id = _read_profile_scalar(profile, "id")
    integration = _read_profile_scalar(profile, "integration")
    image = _read_profile_scalar(profile, "image")
    if any(ch in image for ch in "\r\n"):
        raise ValueError("runtime image contains a newline")

    if output.exists():
        if not force:
            raise FileExistsError(f"output already exists: {output}")
        shutil.rmtree(output)

    shutil.copytree(
        task,
        output,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".pytest_cache"),
    )

    out_dockerfile = output / "environment" / "Dockerfile"
    lines = out_dockerfile.read_text(encoding="utf-8").splitlines()
    matches = [i for i, line in enumerate(lines) if BASE_ARG_RE.match(line)]
    if len(matches) != 1:
        shutil.rmtree(output, ignore_errors=True)
        raise ValueError(
            "canonical Dockerfile must contain exactly one "
            "'ARG HARNESS_SMOKE_BASE_IMAGE=<default>' line"
        )
    idx = matches[0]
    lines[idx] = f"ARG HARNESS_SMOKE_BASE_IMAGE={image}"
    out_dockerfile.write_text("\n".join(lines) + "\n", encoding="utf-8")

    binding = {
        "schema_version": "0.1",
        "canonical_task": str(task),
        "runtime_profile": str(profile),
        "runtime_profile_id": profile_id,
        "runtime_image": image,
        "integration": integration,
        "resolved_task": str(output),
    }
    (output / ".harness-smoke-binding.json").write_text(
        json.dumps(binding, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return binding


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", type=Path, required=True, help="Canonical Harbor task directory")
    parser.add_argument("--profile", type=Path, required=True, help="Runtime profile YAML")
    parser.add_argument("--output", type=Path, required=True, help="Temporary resolved task directory")
    parser.add_argument("--force", action="store_true", help="Replace an existing output directory")
    parser.add_argument("--json", action="store_true", help="Print binding metadata as JSON")
    args = parser.parse_args(argv)

    try:
        binding = bind_task(args.task, args.profile, args.output, force=args.force)
    except Exception as exc:  # CLI boundary: return a concise actionable error.
        print(f"bind_task: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(binding, sort_keys=True))
    else:
        print(binding["resolved_task"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
