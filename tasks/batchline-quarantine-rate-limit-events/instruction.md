# Quarantine incident rate-limit events

An operational event archive for the August 14 incident is available at:

`operations/incident-2026-08-14.jsonl`

Find every event in that archive that satisfies all of these conditions:

- `worker` is `worker-05`
- `event_type` is `worker.rate_limited`
- `provider` is `images-api`
- `occurred_at` is between `2026-08-14T02:00:00Z` and `2026-08-14T02:40:00Z`, inclusive

Write the matching `event_id` values to `operations/quarantine-events.txt`, one ID per line, in chronological order.

Do not modify the incident archive.
