# Scenario 1 RC2 runtime/clearance prep — v0.2

Candidate task: `batchline-worker-draining-event-extraction` `0.2.0-rc1`.

## Ready locally

- NOP verifier: reward 0.
- RC2 oracle: G1-G6 pass, reward 1.
- Oracle `make check`: pass through G6.
- Schema ownership/reference/test-scope mutation controls: behaving as expected.
- Equivalent absolute worker-schema reference route: passes.
- Public focused layer updated to the six-task v0.2.0 checkpoint including V1.
- Scenario clearance suite resolves one OpenCode 1.18.30 attempt only.
- Runtime regression tests: 9/9 pass.

## Required on the user's Harbor host

1. Harbor NOP.
2. Harbor Oracle.
3. One standard OpenCode 1.18.30 RC2 clearance diagnostic using the matched model/provider setup.
4. Preserve observer, verifier-group artifact, normalized report and trajectory.
5. Review against the task's `EVALUATION_GUIDE.md` and `SCENARIO_1_TASK_CLEARANCE_PROTOCOL_v0_4.md`.

No formal scenario matrix or repeat count is fixed yet.
