#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier /logs/artifacts
python /tests/observe_workspace.py --metadata /tests/smoke_metadata.json --output /logs/artifacts/smoke_observation.json || true
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app/src python /tests/verify.py
status=$?
if [ "$status" -eq 0 ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
exit 0
