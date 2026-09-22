# Scenario 1 RC2 run-evaluation guide

Status: clearance guide for `0.2.0-rc1`. After freeze, the same coding scheme can be used prospectively for formal runs.

## 1. What Scenario 1 is meant to expose

Scenario 1 studies **composition of workspace-interaction pressures under one fixed software target**. Correctness is determined only by the verifier. The research interest is how a harness/model discovers and composes the work needed to reach that target.

Primary pressures:

1. **distributed coordination (B1-calibrated):** worker state, registry/capacity, serializer, CLI, event registry/example and validation behavior must remain synchronized;
2. **substantial extraction/integration (R4-calibrated):** worker constructor ownership moves to `worker_events.py`, compatibility remains through `encoder.py`, and shared event-ID state must not fork;
3. **large structured schema extraction:** five worker definitions move out of the large repeated aggregate schema while job/service definitions remain and aggregate validation still works;
4. **selective structured editing (R1 analogue):** only worker definitions/references among many repeated event-schema regions should move; this is analogous calibration, not an identical R1 operation;
5. **context stewardship:** requirements established during one operation must remain available while the solver works across the others.

V1 provides a supporting baseline for same-process behavioral verification and constrained test artifacts. It does **not** make REPL/persistent execution a preferred route.

## 2. What is not a primary outcome

Do not treat the following as scenario success/failure by themselves:

- number of tests or validation commands;
- edit-tool failures;
- shell versus structured-edit usage;
- whether a persistent interpreter is used;
- token/call/time totals;
- minimal patch size.

Validation and recovery are diagnostic unless they reveal friction in one of the primary pressures. The contract intentionally limits final test work to the one existing schema-location test; unrequested test expansion is a task-clearance warning rather than useful scenario difficulty.

## 3. Evidence layers

Keep four layers separate:

- **Verifier:** contract correctness; the only reward source.
- **Workspace observer:** descriptive final paths/diff footprint.
- **Telemetry:** route/resource totals; descriptive only.
- **Trajectory:** evidence for discovery, edit route, composition, validation and recovery.

A final diff does not reveal the edit mechanism. Non-use of a harness affordance does not imply absence or inability.

## 4. Route coding

For each primary pressure, code only supported trajectory evidence:

- **natural:** taken successfully without visible reformulation/friction;
- **friction:** visible retry/reformulation/local recovery;
- **attempted-failed:** tried but not successfully used;
- **bypassed:** another valid route was chosen;
- **not-evidenced:** no supported conclusion.

### Orientation/localization

Record how the run maps the worker/event/schema surfaces, where it discovers the existing worker-event family and schema ownership, and any wrong ownership assumptions/corrections.

### Editing/extraction

Record the actual operation route, especially:

- how the substantial worker-schema region is localized and moved;
- how non-worker schema content is preserved;
- how worker constructor extraction/removal and compatibility exports are performed;
- whether the solver uses whole-file rewrites, local replacements, line/range edits, scripts/parsers, shell operations, or combinations.

Do **not** expect an edit primitive to fail. The question is whether the physical operation shape changes route choice or makes some route awkward enough to be reformulated.

### Coordination and context stewardship

Track whether previously established requirements are retained across the distributed feature work and the two extraction surfaces. Re-reading after a meaningful workspace change can be appropriate; repeated rediscovery without state change is different evidence.

### Verification/recovery

Record targeted tests, repository-native checks, independent probes and negative controls when present. Distinguish:

- product/contract defects;
- edit/integration defects;
- self-authored verification mistakes;
- environment/tooling problems.

A solver-created validation error is not automatically evidence of product difficulty.

## 5. Focused comparison rules

Use matched focused runs as calibration, not rankings or causal proof.

- B1 can contextualize distributed coordination.
- R4 can contextualize extraction/movement/edit-shape choices.
- R1 can contextualize selective anchoring/preservation only as an analogue.
- V1 can contextualize how a constrained verification artifact and same-process behavior are handled; route uptake may differ and no specific primitive is preferred.

Do not infer that a harness "lost" a capability merely because the scenario route bypasses the tool/route seen in a focused task.

## 6. Clearance decision

A clearance diagnostic passes only if:

- the contract is clear and bounded;
- verifier checks are traceable to stated requirements;
- the main observed workload is concentrated in the intended coordination/extraction/schema pressures;
- the schema split is meaningful rather than a trivial cosmetic rewrite;
- test/validation work remains subordinate to the intended scenario workload;
- no obvious product shortcut bypasses the required structural target;
- failures, if any, are diagnosable rather than produced by hidden verifier assumptions.

A reward-1 run alone is **not** sufficient for task clearance.
