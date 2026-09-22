#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier /logs/artifacts

# Observer must run before verifier. Its output is descriptive only.
python /tests/observe_workspace.py \
  --metadata /tests/scenario_metadata.json \
  --output /logs/artifacts/scenario_workspace_observation.json || true

# Preserve the named verifier-group vector as a first-class scenario artifact.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app/src python /tests/verify.py \
  > /logs/artifacts/scenario_verifier_groups.json
status=$?
cat /logs/artifacts/scenario_verifier_groups.json

if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
exit 0
