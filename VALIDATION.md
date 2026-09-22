# Validation

## Focused suite

Each focused task has untouched-state and author-solution controls plus task-specific verifier sensitivity checks. Runtime/reporting regression tests pass, task/suite/profile TOML files parse, and the current focused `accepted-18` matrix contains 18 passing recorded runs.

## Scenario 1

Scenario 1 keeps solver-visible task version `0.2.0`; workspace observation remains descriptive and does not contribute to reward. Verifier revisions are preserved separately.

The r2 contract correction was validated by reconstructing Custom Attempt 1 from its retained trajectory, reproducing its original r1 G5-only failure, then passing the identical workspace under r2. Mini-SWE Attempt 1 retains its independent G1 lifecycle failure.

Verifier r3 adds two regression guards consistent with the written contract:

- a concrete worker event definition retained in aggregate `$defs` fails even if it is renamed;
- registry drain/resume return and stored snapshots must preserve the identity/service/queue/timestamp/active-job/capacity fields named by the instruction.

A direct external worker `$ref` with a harmless `type: object` sibling passes r3. The author solution passes G1-G6 under r3. Targeted renamed-definition and altered-registry-return mutations fail as intended. These r3 checks do not change any recorded Scenario 1 result.

Runtime/reporting regression tests and package consistency checks are run again when the release artifacts are assembled.
