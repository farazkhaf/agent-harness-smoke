#!/usr/bin/env python
"""Print a detailed deterministic Batchline deployment report."""

from __future__ import annotations

import argparse
from pathlib import Path

from batchline.config.loader import DEFAULT_CONFIG_DIR
from batchline.config.reporting import build_deployment_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default="production")
    parser.add_argument("--config-dir", type=Path, default=DEFAULT_CONFIG_DIR)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_deployment_report(args.environment, config_dir=args.config_dir)
    text = report.text() + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
