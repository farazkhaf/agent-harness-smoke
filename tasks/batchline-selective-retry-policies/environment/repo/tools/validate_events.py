#!/usr/bin/env python
"""Validate JSON event fixtures under a file or directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from batchline.events.validation import registry_schema_errors, validation_errors


def iter_json_paths(target: Path):
    if target.is_file():
        yield target
        return
    yield from sorted(target.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    args = parser.parse_args()

    failures = 0
    registry_errors = registry_schema_errors()
    for error in registry_errors:
        failures += 1
        print(f"EVENT_REGISTRY_INVALID error={error}")

    checked = 0
    for path in iter_json_paths(args.target):
        checked += 1
        document = json.loads(path.read_text(encoding="utf-8"))
        errors = validation_errors(document)
        if errors:
            failures += 1
            for error in errors:
                print(f"EVENT_INVALID file={path} error={error}")
        else:
            print(f"EVENT_OK file={path}")

    if failures:
        print(f"EVENT_VALIDATION_FAILED files={checked} failures={failures}")
        return 1
    print(f"EVENT_VALIDATION_OK files={checked} registry=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
