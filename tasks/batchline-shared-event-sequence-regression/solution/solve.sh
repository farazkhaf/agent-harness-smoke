#!/usr/bin/env bash
set -euo pipefail
cd /app
python - <<'PY'
from pathlib import Path
p = Path('src/batchline/events/encoder.py')
s = p.read_text()
s = s.replace(
    '_SEQUENCES: dict[str, count] = {}\n\n\ndef _event_id(prefix: str) -> str:\n    sequence = _SEQUENCES.setdefault(prefix, count(1))\n    return f"{prefix}_{next(sequence):06d}"\n',
    '_SEQUENCE = count(1)\n\n\ndef _event_id(prefix: str) -> str:\n    return f"{prefix}_{next(_SEQUENCE):06d}"\n',
)
p.write_text(s)
PY
cat > tests/events/test_event_sequence.py <<'PY'
from batchline.config.models import ServiceConfig
from batchline.events.encoder import job_event, service_config_loaded_event, worker_heartbeat_event
from batchline.workers.models import WorkerSnapshot


def test_event_id_sequence_is_shared_across_families(queued_job, fixed_time):
    worker = WorkerSnapshot(
        name="thumb-sequence-test",
        service="thumbnailer",
        queue="media",
        last_seen_at=fixed_time,
        active_jobs=1,
        capacity=4,
    )
    config = ServiceConfig(
        name="thumbnailer",
        queue="media",
        concurrency=4,
        timeout_seconds=120,
        max_retries=4,
        enabled=True,
    )
    events = [
        job_event(queued_job, occurred_at=fixed_time),
        worker_heartbeat_event(worker, occurred_at=fixed_time),
        service_config_loaded_event(config, environment="test", occurred_at=fixed_time),
        job_event(queued_job, occurred_at=fixed_time),
    ]
    sequence = [int(event.event_id.rsplit("_", 1)[1]) for event in events]
    assert sequence == list(range(sequence[0], sequence[0] + len(sequence)))
PY
