# Scenario 1 RC2 task-clearance protocol — v0.4

Candidate: `agent-harness-smoke/batchline-worker-draining-event-extraction` `0.2.0-rc1`.

Task clearance happens **before** formal scenario research collection. Clearance runs may be invalidated by task refinement and must not be used as canonical comparative evidence.

## C0 — local author controls

Require before Harbor diagnostics:

- untouched/NOP reward 0;
- oracle reward 1 with G1-G6 pass;
- repository-native `make check` passes on the oracle;
- workspace observer runs before verifier;
- mutation controls cover lifecycle/capacity, worker constructor ownership, shared event-ID state, schema compatibility, dedicated worker-schema ownership, test/docs scope, and representative example integrity;
- at least one alternate valid implementation/reference form passes where the contract leaves that choice open.

## C1/C2 — Harbor controls

Run Harbor NOP and Harbor Oracle against the exact candidate package. Preserve their artifacts as author controls, not research cells.

## C3 — one diagnostic solver run

Run exactly one standard OpenCode 1.18.30 diagnostic with the matched GLM-5.3-Flash provider/model setup. Identity: `clearance-opencode-rc2-01` (or an equivalent clearly non-canonical label).

Do not add repeats or another harness merely because the diagnostic is interesting. The purpose is task coherence.

## C4 — pressure-location review

Review the diagnostic against the task-specific `EVALUATION_GUIDE.md`.

Clearance requires more than reward 1. Check that:

1. B1-like distributed coordination is genuinely present;
2. the Python worker extraction and large worker-schema extraction create substantial structural workspace work rather than cosmetic edits;
3. selective/preservation-sensitive schema work appears naturally around worker versus non-worker regions;
4. context stewardship is exercised across these operations;
5. optional testing does not become a competing workload—the only final test-source change allowed is the named existing validation test;
6. verifier failures, if any, diagnose stated contract clauses rather than unstated oracle/source assumptions;
7. no obvious shortcut bypasses the required final ownership/compatibility structure.

Tool failure is **not** required. A successful large/local edit is still evidence of a route choice. The question is how the harness/model chooses to perform the physical operation presented by the task.

## C5 — revise freely if needed

Before freeze there is no evidence-preservation constraint. If C4 finds a task defect, revise instruction/oracle/verifier/workspace as needed, rerun C0-C4, and treat earlier diagnostics as superseded clearance evidence.

## C6 — freeze

Freeze only when:

- controls behave correctly;
- the diagnostic has no unresolved task-design defect;
- contract/verifier coverage is traceable;
- intended pressure is concentrated in the designed operation spine;
- package/version/checksum are fixed.

Only after freeze should the formal harness set, repeats, run order, analysis protocol, and canonical collection IDs be fixed prospectively.
