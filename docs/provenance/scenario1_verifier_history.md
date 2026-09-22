# Scenario 1 verifier history

Scenario 1 keeps solver-visible task version `0.2.0`. The task instruction, seed repository, environment, task metadata, observer, and solution used for the recorded executions were not changed when the verifier was corrected.

## Collection-time verifier

The collection-time verifier (`r1`) rejected Custom Attempt 1 in G5. That workspace placed the concrete worker schemas in `worker-events.schema.json` but retained same-named aggregate `$defs` entries that forwarded to the dedicated schema with `$ref`.

The task contract required concrete worker-schema ownership to move to the dedicated file and required aggregate worker variants to resolve through that schema. It did not require a single canonical reference layout or prohibit pure forwarding aliases. The collection-time G5 check therefore enforced a narrower structure than the instruction required.

## Current verifier

The current verifier (`r3`) evaluates schema ownership by substantive assertions rather than by one exact `$ref` shape. Pure forwarding aliases are allowed, while concrete worker schema definitions remain forbidden in the aggregate even if renamed. Registry drain/resume checks likewise test the state and preservation requirements named by the task without requiring Python object identity.

The unchanged Custom Attempt 1 workspace passes the current verifier. No agent rerun was used for this adjudication. Mini-SWE Attempt 1 continues to fail G1 because its final workspace permits a non-draining snapshot to retain a drain reason; that behavioral check is unchanged.

## Retained evaluator evidence

`evidence/verifier-revisions/scenario1-v0.2.0/` contains:

- `v1/` — collection-time verifier and original outcomes;
- `v3/` — current verifier and regression controls;
- `r1-to-r3.diff` — direct verifier diff;
- `EXECUTION_SURFACE_SHA256.txt` — execution-surface checksums.
