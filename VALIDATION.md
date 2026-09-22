# Validation

## Focused suite

Each focused task has untouched-state and author-solution controls plus task-specific verifier sensitivity checks. Runtime/reporting regression tests pass, task/suite/profile TOML files parse, and the `accepted-18` checkpoint contains 18 passing recorded runs.

## Scenario 1

Scenario 1 remains solver-visible task version `0.2.0`. The current verifier is `r3`; workspace observation remains descriptive and does not contribute to reward.

The current verifier passes the author solution and preserves the original behavioral checks. Regression controls confirm that:

- concrete worker event definitions retained in aggregate `$defs` fail even when renamed;
- pure forwarding aliases and direct external worker `$ref` entries with harmless generic siblings are accepted;
- registry drain/resume must preserve the state fields named by the instruction;
- Mini-SWE Attempt 1 retains its independent G1 lifecycle failure;
- the unchanged Custom Attempt 1 workspace passes after removal of the original verifier's canonical-reference overconstraint.

The collection-time verifier, current verifier, direct diff, and checksums are retained under `evidence/verifier-revisions/scenario1-v0.2.0/`.
