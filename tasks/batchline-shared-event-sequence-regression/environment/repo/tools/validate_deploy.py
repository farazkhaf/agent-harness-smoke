#!/usr/bin/env python
"""Validate Batchline deployment configuration for one environment."""

from __future__ import annotations

import argparse
from pathlib import Path

from batchline.config.loader import DEFAULT_CONFIG_DIR, effective_service_catalog
from batchline.config.validation import validate_deployment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default="production")
    parser.add_argument("--config-dir", type=Path, default=DEFAULT_CONFIG_DIR)
    args = parser.parse_args()

    diagnostics = validate_deployment(args.environment, config_dir=args.config_dir)
    if diagnostics:
        for diagnostic in diagnostics:
            print(diagnostic.line())
        print(f"VALIDATION_FAILED environment={args.environment} errors={len(diagnostics)}")
        return 1

    catalog = effective_service_catalog(args.environment, config_dir=args.config_dir)
    print(f"VALIDATION_OK environment={args.environment} services={len(catalog.services)}")
    for name, config in sorted(catalog.services.items()):
        print(
            f"SERVICE_OK service={name} queue={config.queue} concurrency={config.concurrency} "
            f"timeout_seconds={config.timeout_seconds} max_retries={config.max_retries}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
