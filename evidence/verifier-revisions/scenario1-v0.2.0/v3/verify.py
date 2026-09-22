from __future__ import annotations

import ast
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

APP = Path(os.environ.get("BATCHLINE_APP", "/app")).resolve()
SRC = APP / "src"
WORKER_EVENTS = SRC / "batchline/events/worker_events.py"
ENCODER = SRC / "batchline/events/encoder.py"
RESUMED_EXAMPLE = APP / "examples/events/worker_resumed.json"
LEGACY_HEARTBEAT = APP / "examples/events/worker_heartbeat.json"
ROOT_SCHEMA = APP / "schemas/events.schema.json"
WORKER_SCHEMA = APP / "schemas/worker-events.schema.json"
VALIDATION_TEST = APP / "tests/events/test_validation.py"

REQUIRED_WORKER_EVENT_FUNCTIONS = {
    "worker_heartbeat_event",
    "worker_rate_limited_event",
    "worker_unavailable_event",
    "worker_draining_event",
    "worker_resumed_event",
}

REQUIRED_WORKER_SCHEMA_DEFS = {
    "WorkerHeartbeatEvent",
    "WorkerUnavailableEvent",
    "WorkerRateLimitedEvent",
    "WorkerDrainingEvent",
    "WorkerResumedEvent",
}

REQUIRED_WORKER_EVENT_TYPES = {
    "worker.heartbeat",
    "worker.unavailable",
    "worker.rate_limited",
    "worker.draining",
    "worker.resumed",
}


class CheckFailure(AssertionError):
    pass


class Blocked(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def expect_raises(exc_type, fn, message: str) -> None:
    try:
        fn()
    except exc_type:
        return
    except Exception as exc:
        raise CheckFailure(f"{message}: raised {type(exc).__name__} instead of {exc_type.__name__}: {exc}") from exc
    raise CheckFailure(message)


def fresh_imports() -> None:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))


def make_snapshot(*, last_seen=None, active_jobs=1, capacity=4):
    fresh_imports()
    from datetime import UTC, datetime
    from batchline.workers.models import WorkerSnapshot

    return WorkerSnapshot(
        name="thumb-01",
        service="thumbnailer",
        queue="media",
        last_seen_at=last_seen or datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
        active_jobs=active_jobs,
        capacity=capacity,
    )


def group_lifecycle() -> None:
    fresh_imports()
    from batchline.workers.models import WorkerSnapshot
    from batchline.workers.registry import WorkerRegistry

    snapshot = make_snapshot()
    require(hasattr(snapshot, "draining") and hasattr(snapshot, "drain_reason"), "WorkerSnapshot must expose draining and drain_reason")
    require(snapshot.draining is False, "legacy WorkerSnapshot construction must default to non-draining")
    require(snapshot.drain_reason is None, "legacy WorkerSnapshot construction must default drain_reason to None")

    expect_raises(
        ValueError,
        lambda: WorkerSnapshot(
            name=snapshot.name,
            service=snapshot.service,
            queue=snapshot.queue,
            last_seen_at=snapshot.last_seen_at,
            active_jobs=snapshot.active_jobs,
            capacity=snapshot.capacity,
            draining=True,
            drain_reason=None,
        ),
        "draining snapshot without a reason must be rejected",
    )
    expect_raises(
        ValueError,
        lambda: WorkerSnapshot(
            name=snapshot.name,
            service=snapshot.service,
            queue=snapshot.queue,
            last_seen_at=snapshot.last_seen_at,
            active_jobs=snapshot.active_jobs,
            capacity=snapshot.capacity,
            draining=True,
            drain_reason="   ",
        ),
        "draining snapshot with a whitespace-only reason must be rejected",
    )
    expect_raises(
        ValueError,
        lambda: WorkerSnapshot(
            name=snapshot.name,
            service=snapshot.service,
            queue=snapshot.queue,
            last_seen_at=snapshot.last_seen_at,
            active_jobs=snapshot.active_jobs,
            capacity=snapshot.capacity,
            draining=False,
            drain_reason="maintenance",
        ),
        "non-draining snapshot retaining a reason must be rejected",
    )

    if not callable(getattr(snapshot, "drain", None)) or not callable(getattr(snapshot, "resume", None)):
        raise CheckFailure("WorkerSnapshot must expose drain(reason) and resume()")

    expect_raises(ValueError, lambda: snapshot.drain("   "), "drain() must reject whitespace-only reasons")
    drained = snapshot.drain("rolling-restart")
    require(drained is not snapshot, "drain() must return a new immutable snapshot")
    require(snapshot.draining is False and snapshot.drain_reason is None, "drain() must not mutate the original snapshot")
    require(drained.draining is True and drained.drain_reason == "rolling-restart", "drain() did not retain drain state/reason")
    for attr in ("name", "service", "queue", "last_seen_at", "active_jobs", "capacity"):
        require(getattr(drained, attr) == getattr(snapshot, attr), f"drain() changed preserved field {attr}")

    resumed = drained.resume()
    require(resumed is not drained, "resume() must return a new immutable snapshot")
    require(resumed.draining is False and resumed.drain_reason is None, "resume() must clear drain state/reason")
    for attr in ("name", "service", "queue", "last_seen_at", "active_jobs", "capacity"):
        require(getattr(resumed, attr) == getattr(snapshot, attr), f"resume() changed preserved field {attr}")

    registry = WorkerRegistry([snapshot])
    if not callable(getattr(registry, "drain", None)) or not callable(getattr(registry, "resume", None)):
        raise CheckFailure("WorkerRegistry must expose drain(name, reason) and resume(name)")
    stored_drained = registry.drain(snapshot.name, "maintenance")
    registered_drained = registry.get(snapshot.name)
    require(stored_drained.draining and stored_drained.drain_reason == "maintenance", "registry.drain() returned incorrect state")
    require(registered_drained.draining and registered_drained.drain_reason == "maintenance", "registry.drain() did not update the stored snapshot")
    for attr in ("name", "service", "queue", "last_seen_at", "active_jobs", "capacity"):
        require(getattr(stored_drained, attr) == getattr(snapshot, attr), f"registry.drain() returned snapshot changed preserved field {attr}")
        require(getattr(registered_drained, attr) == getattr(snapshot, attr), f"registry.drain() stored snapshot changed preserved field {attr}")
    stored_resumed = registry.resume(snapshot.name)
    registered_resumed = registry.get(snapshot.name)
    require(not stored_resumed.draining and stored_resumed.drain_reason is None, "registry.resume() returned incorrect state")
    require(not registered_resumed.draining and registered_resumed.drain_reason is None, "registry.resume() did not update the stored snapshot")
    for attr in ("name", "service", "queue", "last_seen_at", "active_jobs", "capacity"):
        require(getattr(stored_resumed, attr) == getattr(snapshot, attr), f"registry.resume() returned snapshot changed preserved field {attr}")
        require(getattr(registered_resumed, attr) == getattr(snapshot, attr), f"registry.resume() stored snapshot changed preserved field {attr}")


def group_capacity_health() -> None:
    fresh_imports()
    from datetime import UTC, datetime
    from batchline.workers.health import HealthPolicy, WorkerHealth
    from batchline.workers.registry import WorkerRegistry

    snapshot = make_snapshot(active_jobs=1, capacity=4)
    if not hasattr(snapshot, "drain"):
        raise Blocked("worker drain lifecycle is unavailable")
    other = type(snapshot)(
        name="notify-01",
        service="notify",
        queue="notifications",
        last_seen_at=snapshot.last_seen_at,
        active_jobs=2,
        capacity=8,
    )
    registry = WorkerRegistry([snapshot, other])
    require(snapshot.available_slots == 3, "ordinary available_slots changed unexpectedly")
    require(registry.total_available_slots() == 9, "ordinary registry capacity changed unexpectedly")

    drained = registry.drain(snapshot.name, "maintenance")
    require(drained.capacity == 4 and drained.active_jobs == 1, "draining must preserve physical capacity and active jobs")
    require(drained.available_slots == 0, "draining worker must expose zero available slots")
    require(registry.total_available_slots() == 6, "registry capacity must exclude draining worker free slots")

    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    health = HealthPolicy().classify(drained, now=now)
    require(health is WorkerHealth.HEALTHY, "draining must remain independent of heartbeat health")

    resumed = registry.resume(snapshot.name)
    require(resumed.available_slots == 3, "resume must restore ordinary available slots")
    require(registry.total_available_slots() == 9, "resume must restore registry capacity contribution")


def group_public_surfaces() -> None:
    fresh_imports()
    from datetime import UTC, datetime
    from batchline.api.serializers.workers import serialize_worker_snapshot
    import batchline.cli.commands.workers as worker_commands
    from batchline.cli.render.workers import render_worker_row, render_worker_table
    from batchline.workers.registry import WorkerRegistry

    drain_worker = getattr(worker_commands, "drain_worker", None)
    list_workers = getattr(worker_commands, "list_workers", None)
    resume_worker = getattr(worker_commands, "resume_worker", None)
    require(callable(drain_worker) and callable(list_workers) and callable(resume_worker), "worker command helpers drain_worker/list_workers/resume_worker are incomplete")

    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    snapshot = make_snapshot(last_seen=now)
    if not hasattr(snapshot, "drain"):
        raise Blocked("worker drain lifecycle is unavailable")

    ordinary = serialize_worker_snapshot(snapshot, now=now)
    require(ordinary.get("draining") is False, "serializer must expose draining=False for accepting workers")
    require("drain_reason" in ordinary and ordinary["drain_reason"] is None, "serializer must expose drain_reason=None for accepting workers")
    require(ordinary.get("health") == "healthy", "serializer health semantics changed")

    drained = snapshot.drain("rolling-restart")
    data = serialize_worker_snapshot(drained, now=now)
    require(data.get("draining") is True and data.get("drain_reason") == "rolling-restart", "serializer did not expose draining state/reason")

    ordinary_row = render_worker_row(snapshot, now=now)
    drained_row = render_worker_row(drained, now=now)
    table = render_worker_table((snapshot, drained), now=now)
    require("accepting" in ordinary_row and "-" in ordinary_row, "ordinary CLI row must show accepting state and no reason")
    require("draining" in drained_row and "rolling-restart" in drained_row, "draining CLI row must show state and reason")
    require("healthy" in drained_row, "CLI must continue to show heartbeat health separately")
    require("STATE" in table.splitlines()[0] and "REASON" in table.splitlines()[0], "worker table must expose STATE and REASON columns")

    registry = WorkerRegistry([snapshot])
    require(drain_worker(registry, snapshot.name, "maintenance") == "Draining thumb-01: maintenance", "drain_worker() message/behavior mismatch")
    require(registry.get(snapshot.name).draining is True, "drain_worker() must perform the registry transition")
    listing = list_workers(registry, now=now)
    require("thumb-01" in listing and "draining" in listing and "maintenance" in listing, "list_workers() must render current draining state")
    require(resume_worker(registry, snapshot.name) == "Resumed thumb-01", "resume_worker() message/behavior mismatch")
    require(registry.get(snapshot.name).draining is False, "resume_worker() must perform the registry transition")


def defined_function_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def group_event_structure() -> None:
    require(WORKER_EVENTS.exists(), "src/batchline/events/worker_events.py was not created")
    require(ENCODER.exists(), "src/batchline/events/encoder.py is missing")

    worker_defs = defined_function_names(WORKER_EVENTS)
    encoder_defs = defined_function_names(ENCODER)
    missing = REQUIRED_WORKER_EVENT_FUNCTIONS - worker_defs
    require(not missing, f"worker_events.py does not implement required worker constructors: {sorted(missing)}")
    duplicated = REQUIRED_WORKER_EVENT_FUNCTIONS & encoder_defs
    require(not duplicated, f"encoder.py still defines worker event constructors: {sorted(duplicated)}")

    fresh_imports()
    import batchline.events.encoder as encoder
    import batchline.events.worker_events as worker_events

    for name in sorted(REQUIRED_WORKER_EVENT_FUNCTIONS):
        enc_fn = getattr(encoder, name, None)
        new_fn = getattr(worker_events, name, None)
        require(callable(enc_fn), f"batchline.events.encoder no longer exports {name}")
        require(callable(new_fn), f"batchline.events.worker_events does not export {name}")
        require(enc_fn is new_fn, f"encoder compatibility path for {name} is not the worker_events implementation")
        source = inspect.getsourcefile(new_fn)
        require(source is not None and Path(source).resolve() == WORKER_EVENTS.resolve(), f"{name} implementation is not owned by worker_events.py")

    # Fresh interpreter: extraction must not create a second event-id counter.
    # Consume earlier IDs first so the check verifies relative same-process ordering
    # rather than assuming that the first observed value is 1.
    code = r'''
from datetime import UTC, datetime
from batchline.config.models import ServiceConfig
from batchline.events.encoder import service_config_loaded_event, worker_heartbeat_event, service_config_rejected_event
from batchline.workers.models import WorkerSnapshot
now = datetime(2026, 1, 1, tzinfo=UTC)
config = ServiceConfig(name="thumbnailer", queue="media", concurrency=4, timeout_seconds=120, max_retries=4)
worker = WorkerSnapshot(name="thumb-01", service="thumbnailer", queue="media", last_seen_at=now, active_jobs=1, capacity=4)
for _ in range(5):
    service_config_loaded_event(config, environment="production", occurred_at=now)
e1 = service_config_loaded_event(config, environment="production", occurred_at=now)
e2 = worker_heartbeat_event(worker, occurred_at=now)
e3 = service_config_rejected_event("thumbnailer", environment="production", errors=["x"], occurred_at=now)
print(e1.event_id, e2.event_id, e3.event_id)
'''
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    result = subprocess.run([sys.executable, "-c", code], cwd=APP, env=env, text=True, capture_output=True)
    require(result.returncode == 0, f"event constructors are not import-compatible after extraction: {result.stderr.strip()}")
    ids = result.stdout.strip().split()
    require(len(ids) == 3, f"unexpected event-id probe output: {result.stdout!r}")
    suffixes = [int(item.rsplit("_", 1)[-1]) for item in ids]
    require(suffixes[1] == suffixes[0] + 1 and suffixes[2] == suffixes[1] + 1, f"worker/non-worker event constructors no longer share one event-id sequence: {ids}")


def _worker_schema_ref_matches(ref: object, name: str) -> bool:
    return isinstance(ref, str) and ref.endswith(f"worker-events.schema.json#/$defs/{name}")


def _is_pure_worker_forwarding_alias(definition: object, name: str) -> bool:
    """Return True for a local $defs entry that only forwards ownership externally.

    JSON Schema annotations do not assert worker-event structure, so they may
    accompany the forwarding $ref without making the aggregate schema the
    concrete owner of the definition.
    """
    if not isinstance(definition, dict):
        return False
    if not _worker_schema_ref_matches(definition.get("$ref"), name):
        return False
    allowed = {"$ref", "$comment", "title", "description", "default", "examples", "deprecated", "readOnly", "writeOnly"}
    return set(definition) <= allowed


def _aggregate_reaches_worker_definition(schema: dict, name: str) -> bool:
    """Accept a direct external variant or a local pure forwarding alias."""
    refs = [item.get("$ref") for item in schema.get("oneOf", []) if isinstance(item, dict)]
    if any(_worker_schema_ref_matches(ref, name) for ref in refs):
        return True
    local_ref = f"#/$defs/{name}"
    if local_ref not in refs:
        return False
    return _is_pure_worker_forwarding_alias(schema.get("$defs", {}).get(name), name)


def group_event_contract() -> None:
    fresh_imports()
    import batchline.events.encoder as encoder
    from batchline.events.registry import event_type_info, is_supported_event_type
    required = ["worker_draining_event", "worker_heartbeat_event", "worker_rate_limited_event", "worker_resumed_event", "worker_unavailable_event"]
    missing = [name for name in required if not callable(getattr(encoder, name, None))]
    require(not missing, f"encoder compatibility exports are incomplete: {missing}")
    worker_draining_event = encoder.worker_draining_event
    worker_heartbeat_event = encoder.worker_heartbeat_event
    worker_rate_limited_event = encoder.worker_rate_limited_event
    worker_resumed_event = encoder.worker_resumed_event
    worker_unavailable_event = encoder.worker_unavailable_event
    from batchline.events.validation import load_event_schema, registry_schema_errors, schema_event_types, validate_event

    snapshot = make_snapshot()
    if not hasattr(snapshot, "drain"):
        raise Blocked("worker drain lifecycle is unavailable")
    drained = snapshot.drain("rolling-restart")

    heartbeat = worker_heartbeat_event(drained, occurred_at=snapshot.last_seen_at).to_dict()
    require(heartbeat["payload"].get("draining") is True, "generated heartbeat must include current draining=True state")
    ordinary_heartbeat = worker_heartbeat_event(snapshot, occurred_at=snapshot.last_seen_at).to_dict()
    require(ordinary_heartbeat["payload"].get("draining") is False, "generated heartbeat must include draining=False for accepting workers")

    require(ROOT_SCHEMA.exists(), "aggregate events schema is missing")
    require(WORKER_SCHEMA.exists(), "schemas/worker-events.schema.json was not created")
    schema = load_event_schema(ROOT_SCHEMA)
    worker_schema = load_event_schema(WORKER_SCHEMA)

    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(worker_schema)

    root_definitions = schema.get("$defs", {})
    root_defs = set(root_definitions)
    worker_defs = set(worker_schema.get("$defs", {}))
    concrete_local_worker_defs = [
        name for name in REQUIRED_WORKER_SCHEMA_DEFS
        if name in root_definitions and not _is_pure_worker_forwarding_alias(root_definitions[name], name)
    ]
    require(
        not concrete_local_worker_defs,
        f"aggregate schema retains concrete worker event definitions: {sorted(concrete_local_worker_defs)}",
    )
    require(REQUIRED_WORKER_SCHEMA_DEFS <= worker_defs, f"dedicated worker schema is missing definitions: {sorted(REQUIRED_WORKER_SCHEMA_DEFS - worker_defs)}")
    root_event_types = set()
    concrete_worker_event_types = set()
    for definition in schema.get("$defs", {}).values():
        if isinstance(definition, dict):
            event_type = definition.get("properties", {}).get("event_type", {})
            if isinstance(event_type, dict) and isinstance(event_type.get("const"), str):
                value = event_type["const"]
                root_event_types.add(value)
                if value in REQUIRED_WORKER_EVENT_TYPES:
                    concrete_worker_event_types.add(value)
    require(
        not concrete_worker_event_types,
        f"aggregate schema retains concrete worker event definitions under local names: {sorted(concrete_worker_event_types)}",
    )
    require({"job.queued", "job.started", "job.succeeded", "job.failed", "job.canceled", "job.retry_scheduled", "service.config_loaded", "service.config_rejected"} <= root_event_types, "aggregate schema no longer owns required job/service event definitions")

    for name in REQUIRED_WORKER_SCHEMA_DEFS:
        require(
            _aggregate_reaches_worker_definition(schema, name),
            f"aggregate worker variant does not resolve to dedicated {name}",
        )

    heartbeat_payload_schema = worker_schema["$defs"]["WorkerHeartbeatEvent"]["properties"]["payload"]
    require("draining" in heartbeat_payload_schema["properties"], "heartbeat schema does not accept draining")
    require("draining" not in heartbeat_payload_schema["required"], "heartbeat schema must keep draining optional for legacy documents")
    validate_event(heartbeat)
    validate_event(ordinary_heartbeat)

    legacy = json.loads(json.dumps(ordinary_heartbeat))
    legacy["payload"].pop("draining", None)
    validate_event(legacy)
    if LEGACY_HEARTBEAT.exists():
        validate_event(json.loads(LEGACY_HEARTBEAT.read_text(encoding="utf-8")))

    derived = worker_draining_event(drained, occurred_at=snapshot.last_seen_at).to_dict()
    require(derived["payload"]["reason"] == "rolling-restart", "draining event must derive reason from a drained snapshot when omitted")
    validate_event(derived)

    matching_explicit = worker_draining_event(
        drained,
        reason="rolling-restart",
        occurred_at=snapshot.last_seen_at,
    ).to_dict()
    require(matching_explicit["payload"]["reason"] == "rolling-restart", "matching explicit/snapshot drain reasons must remain valid")
    validate_event(matching_explicit)

    # Existing moved constructors must preserve envelope arguments after extraction.
    custom_source = "batchline.custom-worker-source"
    envelope_checks = [
        worker_heartbeat_event(snapshot, occurred_at=snapshot.last_seen_at, source=custom_source).to_dict(),
        worker_rate_limited_event(
            snapshot,
            provider="images-api",
            limit_name="requests-per-minute",
            occurred_at=snapshot.last_seen_at,
            source=custom_source,
        ).to_dict(),
        worker_unavailable_event(
            snapshot,
            unavailable_seconds=240,
            occurred_at=snapshot.last_seen_at,
            source=custom_source,
        ).to_dict(),
        worker_draining_event(
            snapshot,
            reason="legacy-reason",
            occurred_at=snapshot.last_seen_at,
            source=custom_source,
        ).to_dict(),
    ]
    expected_time = snapshot.last_seen_at.isoformat().replace("+00:00", "Z")
    for event in envelope_checks:
        require(event["source"] == custom_source, f"{event['event_type']} no longer preserves the source argument")
        require(event["occurred_at"] == expected_time, f"{event['event_type']} no longer preserves the occurred_at argument")
        validate_event(event)

    legacy_call = worker_draining_event(snapshot, reason="legacy-reason", occurred_at=snapshot.last_seen_at).to_dict()
    require(legacy_call["payload"]["reason"] == "legacy-reason", "legacy explicit-reason worker_draining_event call no longer works")
    validate_event(legacy_call)

    expect_raises(ValueError, lambda: worker_draining_event(snapshot, reason="   "), "empty explicit drain-event reason must be rejected")
    expect_raises(ValueError, lambda: worker_draining_event(drained, reason="different"), "explicit reason disagreeing with snapshot state must be rejected")
    expect_raises(ValueError, lambda: worker_draining_event(snapshot), "non-draining snapshot without explicit reason must be rejected")

    resumed = drained.resume()
    resumed_event = worker_resumed_event(resumed, occurred_at=snapshot.last_seen_at).to_dict()
    require(resumed_event["event_type"] == "worker.resumed", "worker_resumed_event has wrong event type")
    require(resumed_event["payload"] == {
        "worker": "thumb-01",
        "service": "thumbnailer",
        "queue": "media",
        "active_jobs": 1,
        "capacity": 4,
    }, "worker.resumed payload does not match the contract")
    validate_event(resumed_event)
    expect_raises(ValueError, lambda: worker_resumed_event(drained), "worker_resumed_event must reject a still-draining snapshot")

    require(is_supported_event_type("worker.resumed"), "worker.resumed is not registered")
    require(event_type_info("worker.resumed").domain == "worker", "worker.resumed must be registered in the worker domain")
    require(registry_schema_errors() == (), "event registry and schema are out of sync")
    require({"worker.heartbeat", "worker.unavailable", "worker.rate_limited", "worker.draining", "worker.resumed"} <= set(schema_event_types()), "aggregate schema type discovery does not include all worker event types after the split")
    require("WorkerResumedEvent" in worker_schema["$defs"], "worker schema is missing WorkerResumedEvent")
    resumed_schema = worker_schema["$defs"]["WorkerResumedEvent"]
    require(resumed_schema.get("additionalProperties") is False, "WorkerResumedEvent must remain a strict object schema")
    resumed_payload_schema = resumed_schema.get("properties", {}).get("payload", {})
    require(resumed_payload_schema.get("additionalProperties") is False, "worker.resumed payload schema must reject undeclared fields")

    require(RESUMED_EXAMPLE.exists(), "examples/events/worker_resumed.json was not added")
    resumed_example = json.loads(RESUMED_EXAMPLE.read_text(encoding="utf-8"))
    require(resumed_example.get("event_type") == "worker.resumed", "worker_resumed.json must be a representative worker.resumed example")
    validate_event(resumed_example)

    limited = worker_rate_limited_event(
        snapshot,
        provider="images-api",
        limit_name="requests-per-minute",
        occurred_at=snapshot.last_seen_at,
        detail={"bucket": "standard"},
    ).to_dict()
    unavailable = worker_unavailable_event(snapshot, unavailable_seconds=240, occurred_at=snapshot.last_seen_at).to_dict()
    require(limited["event_type"] == "worker.rate_limited" and limited["payload"]["provider"] == "images-api", "worker.rate_limited behavior changed during extraction")
    require(unavailable["event_type"] == "worker.unavailable" and unavailable["payload"]["unavailable_seconds"] == 240, "worker.unavailable behavior changed during extraction")
    validate_event(limited)
    validate_event(unavailable)



def group_integration_preservation() -> None:
    fresh_imports()
    from datetime import UTC, datetime
    from batchline.api.serializers.workers import serialize_worker_snapshot
    import batchline.cli.commands.workers as worker_commands
    from batchline.cli.render.workers import render_worker_row
    import batchline.events.encoder as encoder
    from batchline.events.validation import validate_event
    from batchline.workers.health import HealthPolicy, WorkerHealth
    from batchline.workers.registry import WorkerRegistry

    now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    snapshot = make_snapshot(last_seen=now)
    if not hasattr(snapshot, "drain"):
        raise Blocked("worker drain lifecycle is unavailable")
    drain_worker = getattr(worker_commands, "drain_worker", None)
    resume_worker = getattr(worker_commands, "resume_worker", None)
    worker_draining_event = getattr(encoder, "worker_draining_event", None)
    worker_heartbeat_event = getattr(encoder, "worker_heartbeat_event", None)
    worker_resumed_event = getattr(encoder, "worker_resumed_event", None)
    if not all(callable(x) for x in (drain_worker, resume_worker, worker_draining_event, worker_heartbeat_event, worker_resumed_event)):
        raise Blocked("required command/event integration surfaces are unavailable")
    registry = WorkerRegistry([snapshot])
    require(registry.total_available_slots() == 3, "integration precondition: normal capacity is incorrect")

    require(drain_worker(registry, snapshot.name, "maintenance") == "Draining thumb-01: maintenance", "integration drain command failed")
    drained = registry.get(snapshot.name)
    require(drained.available_slots == 0 and registry.total_available_slots() == 0, "integration drain did not remove new-work capacity")
    require(HealthPolicy().classify(drained, now=now) is WorkerHealth.HEALTHY, "integration drain incorrectly changed heartbeat health")
    serial = serialize_worker_snapshot(drained, now=now)
    require(serial["draining"] is True and serial["drain_reason"] == "maintenance", "integration serializer is inconsistent with registry state")
    require("healthy" in render_worker_row(drained, now=now) and "draining" in render_worker_row(drained, now=now), "integration CLI output is inconsistent with registry state")
    validate_event(worker_heartbeat_event(drained, occurred_at=now).to_dict())
    validate_event(worker_draining_event(drained, occurred_at=now).to_dict())

    require(resume_worker(registry, snapshot.name) == "Resumed thumb-01", "integration resume command failed")
    resumed = registry.get(snapshot.name)
    require(resumed.available_slots == 3 and registry.total_available_slots() == 3, "integration resume did not restore capacity")
    require(resumed.drain_reason is None and not resumed.draining, "integration resume did not clear drain state")
    validate_event(worker_resumed_event(resumed, occurred_at=now).to_dict())

    require(VALIDATION_TEST.exists(), "tests/events/test_validation.py is missing")
    validation_test_defs = defined_function_names(VALIDATION_TEST)
    require("test_event_schemas_are_loadable_and_worker_definitions_are_split" in validation_test_defs, "required updated schema-ownership test is missing")
    require("test_example_event_is_valid" in validation_test_defs and "test_invalid_status_is_rejected" in validation_test_defs, "existing validation tests were not kept intact")

    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=APP, text=True, capture_output=True)
    require(status.returncode == 0, f"unable to inspect final workspace scope: {status.stderr.strip()}")
    for line in status.stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        require(not path.startswith("docs/"), f"documentation changes are out of scope: {path}")
        if path.startswith("tests/"):
            require(path == "tests/events/test_validation.py", f"only tests/events/test_validation.py may change under tests/: {path}")

    env = {**os.environ, "PYTHONPATH": str(SRC)}
    result = subprocess.run(["make", "check"], cwd=APP, env=env, text=True, capture_output=True)
    require(result.returncode == 0, f"repository-native checks failed:\n{result.stdout}\n{result.stderr}")


GROUPS = [
    ("G1_lifecycle", group_lifecycle),
    ("G2_capacity_health", group_capacity_health),
    ("G3_public_surfaces", group_public_surfaces),
    ("G4_event_structure", group_event_structure),
    ("G5_event_contract", group_event_contract),
    ("G6_integration_preservation", group_integration_preservation),
]


def main() -> None:
    results: dict[str, dict[str, str]] = {}
    all_pass = True
    for name, fn in GROUPS:
        try:
            fn()
        except Blocked as exc:
            all_pass = False
            results[name] = {"status": "blocked", "note": str(exc)}
        except CheckFailure as exc:
            all_pass = False
            results[name] = {"status": "fail", "note": str(exc)}
        except Exception as exc:
            all_pass = False
            results[name] = {"status": "error", "note": f"{type(exc).__name__}: {exc}"}
            traceback.print_exc()
        else:
            results[name] = {"status": "pass", "note": ""}

    payload = {"reward": 1 if all_pass else 0, "groups": results}
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
