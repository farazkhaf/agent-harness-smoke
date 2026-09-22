#!/bin/sh
set -eu
ROOT="${1:-/app}"
SELF="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
for rel in \
  src/batchline/workers/models.py \
  src/batchline/workers/registry.py \
  src/batchline/api/serializers/workers.py \
  src/batchline/cli/render/workers.py \
  src/batchline/cli/commands/workers.py \
  src/batchline/events/_common.py \
  src/batchline/events/worker_events.py \
  src/batchline/events/encoder.py \
  src/batchline/events/registry.py \
  schemas/events.schema.json \
  schemas/worker-events.schema.json \
  src/batchline/events/validation.py \
  tests/events/test_validation.py \
  examples/events/worker_resumed.json
do
  mkdir -p "$ROOT/$(dirname "$rel")"
  cp "$SELF/$rel" "$ROOT/$rel"
done
