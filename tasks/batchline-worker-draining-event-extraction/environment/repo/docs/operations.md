# Operational archives

Batchline operational archives are newline-delimited JSON (`.jsonl`) exports intended for incident review, audit retention, and local replay preparation. Each line is one independent event record. Large archives should be processed as streams rather than loaded into memory as one JSON document.

`batchline.operations.iter_archive()` yields typed records one line at a time. `matching_event_ids()` provides a small reference implementation for filtering by worker, event type, provider, and time range. The `tools/generate_event_archive.py` utility produces deterministic local archives for examples and tests.

Operational archives are data artifacts, not the lifecycle-event JSON Schema itself. They may contain a reduced set of fields chosen for operational review.
