# Scenario 1 verification-role map

This map applies conventional **pass-to-pass (P2P)** and **fail-to-pass (F2P)** vocabulary at the requirement/assertion level. It is descriptive documentation; verifier reward logic remains G1-G6 and is unchanged from the cleared candidate.

## F2P roles — required new behavior/structure

- `WorkerSnapshot.draining` / `drain_reason` state model and invalid-state rejection.
- immutable `drain(reason)` / `resume()` transitions.
- registry drain/resume operations and draining-capacity semantics.
- serializer drain fields and CLI STATE/REASON plus drain/resume command helpers.
- worker-event implementation ownership in `events/worker_events.py`.
- new compatibility export `worker_resumed_event`.
- generated heartbeat `draining` field.
- evolved optional-reason behavior for `worker_draining_event`.
- `worker.resumed` registration, constructor, strict schema and example.
- dedicated `schemas/worker-events.schema.json` ownership for the five worker event definitions.
- aggregate external worker references and cross-schema validation/type discovery.
- renamed/updated schema-location test in `tests/events/test_validation.py`.

## P2P roles — seed behavior that must continue to pass

- legacy `WorkerSnapshot(...)` construction without drain fields.
- ordinary non-draining capacity calculation and registry totals.
- heartbeat-age health semantics, including health remaining independent of operational drain state.
- existing serializer/CLI health information.
- existing public worker-event imports through `batchline.events.encoder`.
- one process-wide event-ID sequence across worker and non-worker constructors.
- existing `occurred_at` and `source` envelope behavior.
- legacy heartbeat documents without `payload.draining` remaining schema-valid.
- existing explicit-reason `worker_draining_event` calls for non-draining/legacy snapshots.
- existing `worker.rate_limited` and `worker.unavailable` behavior.
- job and service/config event definitions remaining owned by the aggregate schema.
- existing validation tests `test_example_event_is_valid` and `test_invalid_status_is_rejected` remaining present.
- repository-native tests and validation commands remaining healthy.
- unrelated docs/tests remaining unchanged as required by the task scope.

## Mixed/integration checks

Some verifier assertions simultaneously exercise new behavior and preservation, so forcing a single label would be misleading. Examples include:

- registry/schema parity after the worker-schema split;
- aggregate validation of both new and legacy worker examples;
- end-to-end drain → serialize/render/event → resume flow;
- compatibility re-exports whose existence is preserved while implementation ownership changes.

Because G1-G6 intentionally compose these assertions, a group-level NOP `fail` or `blocked` status is not itself a P2P/F2P classification.
