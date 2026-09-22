# Scenario 1 formal-run protocol — pre-collection lock template

Status: **task frozen; formal comparison matrix not yet locked**.

Scenario task `agent-harness-smoke/batchline-worker-draining-event-extraction` is frozen at `0.2.0`. Task authoring/clearance evidence must not be mixed with formal comparative runs.

Before the first formal scenario run, record prospectively in this document (or its successor):

1. harness set and exact harness versions;
2. model/provider/configuration matching rule;
3. repeat count per harness cell;
4. invalid-run/replacement rule;
5. random/seed handling where applicable;
6. canonical evidence files retained per run;
7. public/private trajectory boundary;
8. whether any additional harnesses are an initial matrix member or a later extension phase.

Once the first formal run is started, do not change the task instruction, seed environment, verifier, or observer schema for the same comparison phase. Any required change creates a new scenario task version/phase.

## Required retained evidence per run

- Harbor `result.json` and task/runtime metadata;
- normalized report;
- verifier group artifact;
- workspace observer artifact;
- ATIF/native trajectory sufficient to support route claims;
- run/trial identifier and exact task checksum.

## Analysis protocol

Use the frozen task-local `EVALUATION_GUIDE.md` and `VERIFICATION_ROLE_MAP.md`. Analyze correctness first, then workspace/operation shape, route composition and recovery, then descriptive resource telemetry. Do not rank harnesses from call/token/time totals.

## Clearance boundary

The pre-freeze NOP, oracle and OpenCode diagnostic are task-design evidence only. They may be cited as provenance for why the task was frozen, but they are not members of the formal comparison matrix.
