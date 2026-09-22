# Validation — agent-harness-smoke/batchline-worker-draining-event-extraction 0.2.0-rc1

These are authoring/task-clearance controls, not formal comparative research runs.

## Local controls

| Control | Expected/observed result |
|---|---|
| untouched starting state | reward 0; expected foundational groups fail/block |
| primary RC2 oracle | reward 1; G1-G6 pass |
| worker definition copied back into aggregate schema | G5 fails |
| required worker schema definition removed | G5 fails cleanly |
| extra test file added | G6 fails final-scope contract |
| documentation edited | G6 fails final-scope contract |
| required updated schema-ownership test renamed/removed | G6 fails |
| aggregate worker refs changed from relative to equivalent absolute worker-schema URI | all groups pass |
| worker/non-worker event-ID counter split | G4 fails |
| duplicate/proxy worker constructor implementation retained in encoder | G4 fails |
| heartbeat `draining` made schema-required | G5/G6 fail |
| wrong-but-schema-valid resumed example | G5 fails |
| moved constructor drops `source` preservation | G5 fails |
| alternate internal shared-helper layout | all groups should pass |
| repository-native `make check` on oracle | pass |

The absolute-URI control is specifically intended to guard against an oracle-shaped verifier that requires one exact `$ref` spelling.

## Clearance still required on Harbor-capable host

1. Harbor NOP against `0.2.0-rc1`.
2. Harbor Oracle against `0.2.0-rc1`.
3. Exactly one standard OpenCode 1.18.30 diagnostic with the matched GLM-5.3-Flash model/provider configuration.
4. Review that diagnostic for **pressure-location/task coherence**, not OpenCode quality: the substantial Python/schema operations should carry the route/context pressure; optional testing should not become a competing workstream.
5. If a task defect is found, revise freely and repeat controls. Formal evidence preservation begins only after freeze.
