#!/usr/bin/env bash
set -uo pipefail
mkdir -p /logs/verifier /logs/artifacts

# Snapshot externally observable workspace state BEFORE correctness verification.
# Observation is diagnostic only; it does not affect B1 correctness.
OBSERVE_STATUS=0
python /tests/observe_workspace.py \
  --metadata /tests/smoke_metadata.json \
  --output /logs/artifacts/smoke_observation.json || OBSERVE_STATUS=$?

if [ "$OBSERVE_STATUS" -ne 0 ]; then
  printf 'workspace observer failed with status %s\n' "$OBSERVE_STATUS" \
    > /logs/artifacts/smoke_observation_error.txt
fi

# Correctness is behavioral and independent of the observed patch shape.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app/src python /tests/verify.py
VERIFY_STATUS=$?

if [ "$VERIFY_STATUS" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

# Harbor reads the reward file. A verifier failure maps to reward=0 rather than
# making the verifier container itself fail operationally.
exit 0
