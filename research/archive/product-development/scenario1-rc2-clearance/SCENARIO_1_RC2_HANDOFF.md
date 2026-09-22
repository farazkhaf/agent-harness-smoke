# Scenario 1 RC2 clearance handoff

Candidate task: `agent-harness-smoke/batchline-worker-draining-event-extraction` `0.2.0-rc1`.

## What changed from RC1

- kept the worker drain/resume lifecycle and worker Python event extraction;
- added dedicated `schemas/worker-events.schema.json` ownership for five worker event definitions;
- kept `schemas/events.schema.json` as the stable aggregate entry point with external worker references;
- updated aggregate validation/type discovery across the split;
- limited test-source work to the one existing schema-location test;
- prohibited additional test files and documentation changes in the final contract;
- changed the shared event-ID verifier probe to compare relative same-process increments after earlier IDs have already been consumed;
- removed oracle-shaped `$ref`/job-definition-name assumptions from the verifier.

Oracle patch calibration remains author-only: approximately +601/-374 across 14 paths from the anchor. This is not a verifier requirement.

## Local status

- NOP: reward 0.
- Oracle: reward 1, G1-G6 pass.
- Runtime tests: 9/9 pass.
- Clearance suite: one OpenCode 1.18.30 attempt.
- Equivalent absolute worker-schema refs: pass.
- Missing/duplicate worker schema ownership, extra test file, docs change, and required test-name defects: rejected as expected.

## User-host sequence

1. Run Harbor NOP using the new standalone task package.
2. Run Harbor Oracle using the same package.
3. Run one OpenCode clearance diagnostic from the full repository:

```powershell
.\runtime\scripts\run-suite.ps1 `
  -SuitePath "suites\batchline-scenario1-clearance\suite.toml" `
  -TrialsRoot "$PWD\trials" `
  -OutputRoot "$PWD\results\batchline-scenario1\clearance-rc2"
```

Preserve the trial, observer artifact, verifier-group artifact, normalized report and trajectory. Review that run for task coherence using the task-specific `EVALUATION_GUIDE.md`; do not treat it as formal research evidence.
