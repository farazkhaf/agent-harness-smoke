# Task design — batchline-worker-draining-event-extraction 0.2.0

## Purpose

Scenario 1 composes several interaction pressures inside one coherent maintenance change: coordinated worker lifecycle behavior, Python event-constructor extraction, JSON-Schema ownership extraction, preservation-sensitive integration, and bounded verification scope.

The product target is explicit, but the route is not. A solver may choose native file operations, shell tools, scripts, structured parsing, whole-file rewrites, incremental edits, or another valid mechanism.

## Pressure-bearing work

The task requires the solver to:

1. discover worker, registry, CLI, event, schema, example, and validation ownership;
2. implement drain/resume state consistently across those surfaces;
3. move worker event constructors to `worker_events.py` while preserving compatibility and the shared process-wide event-ID sequence;
4. move concrete worker JSON-Schema definitions to `worker-events.schema.json` while keeping the aggregate schema as the public validation entry point;
5. preserve registry/schema parity, legacy heartbeat compatibility, examples, and repository validation;
6. update the named existing schema-location test without expanding test or documentation scope.

Patch size, line count, command count, and tool selection are not task requirements.

## Verifier boundary

The verifier checks stated behavior, required preservation, explicit module/schema ownership, named public surfaces, and the constrained final test/document scope. Structural checks are used only where the instruction makes that structure part of the software contract. Equivalent implementations that satisfy the stated ownership and behavior are accepted even when they differ from the author solution.

Workspace observations and trajectories are descriptive evidence and do not contribute to reward.
