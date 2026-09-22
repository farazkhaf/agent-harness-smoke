# First-class worker draining and worker-event extraction

Batchline already exposes a `worker.draining` lifecycle event, but worker runtime state cannot currently represent whether a worker has stopped accepting new jobs. Complete the drain/resume lifecycle and separate worker event construction from the general event encoder while preserving existing public behavior.

## Worker drain/resume lifecycle

Extend `WorkerSnapshot` with public drain state:

- `draining: bool`, defaulting to `False`;
- `drain_reason: str | None`, defaulting to `None`.

The valid states are:

- a non-draining worker has no drain reason;
- a draining worker has a non-empty drain reason.

Existing `WorkerSnapshot(...)` construction that omits these fields must continue to work.

Add immutable lifecycle methods:

- `WorkerSnapshot.drain(reason)` returns a new draining snapshot;
- `WorkerSnapshot.resume()` returns a new non-draining snapshot and clears the reason.

`drain()` must reject an empty or whitespace-only reason. These transitions must preserve the worker's identity, service, queue, heartbeat timestamp, active-job count, and physical capacity.

A draining worker is alive but is not accepting new work. Therefore:

- `WorkerSnapshot.available_slots` is `0` while draining;
- otherwise it remains `capacity - active_jobs`;
- draining must not change `capacity` or `active_jobs`.

Add `WorkerRegistry.drain(name, reason)` and `WorkerRegistry.resume(name)`. Each operation must update the registry's stored snapshot and return the updated snapshot. Registry capacity totals must reflect the zero available slots of draining workers and return to normal after resume.

Heartbeat health remains a separate concept. `HealthPolicy` must continue to classify workers from heartbeat age; a recently seen worker may be both `healthy` and `draining`.

## Public worker representations and actions

`serialize_worker_snapshot()` must always include:

- `draining`;
- `drain_reason`.

For a non-draining worker these values are `False` and `None`.

Human-readable worker output must continue to show heartbeat health and must also show operational state separately:

- `accepting` for a non-draining worker;
- `draining` for a draining worker;
- the drain reason when draining, and `-` when there is no reason.

The worker table should expose `STATE` and `REASON` columns in addition to the existing information.

Add framework-independent command helpers in `batchline.cli.commands.workers`:

- `drain_worker(registry, name, reason)`, which performs the registry transition and returns `Draining <name>: <reason>`;
- `resume_worker(registry, name)`, which performs the registry transition and returns `Resumed <name>`.

## Worker event module ownership

Create:

`src/batchline/events/worker_events.py`

Worker event constructor implementations must live in this module. It must implement:

- `worker_heartbeat_event`;
- `worker_rate_limited_event`;
- `worker_unavailable_event`;
- `worker_draining_event`;
- `worker_resumed_event`.

`src/batchline/events/encoder.py` must no longer define worker event constructors. Existing supported imports through `batchline.events.encoder` must continue to work, including the four worker event helpers that existed before this change; the new `worker_resumed_event` should also be available there.

Do not leave duplicate or proxy implementations of the worker event constructors in `encoder.py`: implementation ownership must be `worker_events.py`.

The extraction must preserve existing event-envelope behavior. In particular, it must not fork event-ID generation: worker and non-worker event constructors must continue to draw from the same process-wide event-ID sequence. Existing `occurred_at`, `source`, and envelope behavior must remain compatible. How shared event-construction support is organized internally is not prescribed.

## Worker lifecycle events and schema compatibility

Newly generated `worker.heartbeat` events must include the worker's current `draining` boolean in the payload.

Update the event schema to accept that field. It must remain optional in the schema so existing heartbeat event documents that predate the field remain valid.

Evolve `worker_draining_event` compatibly:

- its explicit `reason=` argument becomes optional;
- when called with a draining snapshot and no explicit reason, use the snapshot's `drain_reason`;
- the existing explicit-reason call form must continue to work for callers with a non-draining/legacy snapshot;
- an empty explicit reason must be rejected;
- if a draining snapshot already has a reason and an explicit reason is supplied, the two reasons must agree or the call must be rejected.

Add a `worker.resumed` event:

- register `worker.resumed` as a worker event type;
- `worker_resumed_event(snapshot, ...)` must require a non-draining snapshot;
- its payload contains `worker`, `service`, `queue`, `active_jobs`, and `capacity`;
- add strict JSON Schema coverage for the event.

Add a representative resumed-event example at `examples/events/worker_resumed.json` so the repository's example-event corpus covers the new lifecycle event, and keep the existing example-event validation workflow healthy.

Existing `worker.rate_limited` and `worker.unavailable` behavior must remain intact after the extraction. Registry and schema event-type coverage must remain synchronized.

## Worker schema ownership and aggregate validation

Split worker lifecycle-event schema ownership out of the monolithic aggregate schema.

Create:

`schemas/worker-events.schema.json`

This dedicated Draft 2020-12 schema must own the concrete definitions for all five worker lifecycle events:

- `WorkerHeartbeatEvent`;
- `WorkerUnavailableEvent`;
- `WorkerRateLimitedEvent`;
- `WorkerDrainingEvent`;
- `WorkerResumedEvent`.

The dedicated worker schema must be independently loadable as a valid JSON Schema and must preserve the worker-event compatibility requirements above.

`schemas/events.schema.json` remains the stable aggregate public event schema. Remove the concrete worker event definitions from its local `$defs` and have its worker variants reference `worker-events.schema.json`. Keep the existing job and service/config event definitions owned by the aggregate schema. Existing callers that validate events through the default Batchline event-validation API must not need to know that worker schemas moved to a sibling file.

Registry/schema parity must continue to cover the full aggregate event set across both schema files. The repository's example-event validation must continue to validate worker examples through the aggregate entry point.

Update the existing schema-location test in `tests/events/test_validation.py` so it reflects the new worker-schema ownership, and name it `test_event_schemas_are_loadable_and_worker_definitions_are_split`. Keep the other existing validation tests, `test_example_event_is_valid` and `test_invalid_status_is_rejected`, intact. Do not add new test files, and leave files under `docs/` unchanged.

## Preservation

Preserve ordinary behavior for workers that are never drained, including existing construction, capacity calculations, and heartbeat health semantics.

Preserve existing public worker-event imports and unrelated job/service event behavior.

Repository tests and validation commands must continue to pass. The only test-source file that should change is `tests/events/test_validation.py`; do not add other tests or modify documentation.

The required final state is described above. Search/navigation strategy, edit mechanism, helper-module layout, change order, and validation/recovery route are not prescribed.
