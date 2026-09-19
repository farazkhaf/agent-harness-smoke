#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=/app/src python - <<'PY'
from datetime import UTC, datetime
from pathlib import Path
from batchline.operations import matching_event_ids

ids = matching_event_ids(
    '/app/operations/incident-2026-08-14.jsonl',
    worker='worker-05',
    event_type='worker.rate_limited',
    provider='images-api',
    start_at=datetime(2026, 8, 14, 2, 0, tzinfo=UTC),
    end_at=datetime(2026, 8, 14, 2, 40, tzinfo=UTC),
)
Path('/app/operations/quarantine-events.txt').write_text(''.join(f'{event_id}\n' for event_id in ids), encoding='utf-8')
PY
