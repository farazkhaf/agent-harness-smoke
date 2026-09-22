# Scenario 1 Runtime / Task-Clearance Preparation — v0.2

Status: **pre-freeze task clearance**, not formal research collection.

## Completed in authoring environment

- canonical Harbor task wrapper added (`task.toml`, Dockerfile, setup lock/setup script);
- agent timeout fixed at 600 s and verifier timeout at 180 s;
- workspace observer runs before verifier and remains non-scoring;
- named G1–G6 verifier JSON is preserved as an artifact;
- untouched/NOP local simulation returns reward 0 with diagnostic groups;
- oracle local simulation returns reward 1 with all six groups passing;
- clean anchor repository `make check` passes;
- task TOML/metadata, Python and shell syntax checks pass;
- generic runtime binder resolves the unchanged candidate task for OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6;
- compact reporting can preserve scenario group diagnostics and workspace-observer summaries;
- runtime regression tests pass (9/9).

These checks establish authoring readiness only. They are not Scenario 1 research results.

## Active next steps on a Harbor-capable host

1. Run Harbor NOP against `0.1.0-rc1`.
2. Run Harbor Oracle against the same candidate.
3. Confirm observer and G1–G6 artifacts survive Harbor artifact collection.
4. Run one standard OpenCode 1.18.30 diagnostic attempt (`clearance-opencode-01`).
5. Review that final workspace and trajectory jointly for **task coherence**, not harness evaluation.
6. Refine the task if the run exposes ambiguity, verifier gaps, artificial pressure, accidental oracle-shape constraints, or packaging defects.
7. Repeat author controls after any material change.
8. Freeze/version/checksum the task only after clearance succeeds.

## Research protocol is deliberately deferred

No repeat count or final harness matrix is fixed yet.

Two runs per formal harness is a live candidate, especially if the eventual matrix expands beyond the three focused-suite harnesses, but this should be decided only after task clearance and before formal comparative data collection.

OpenHands, Codex, or another harness may be considered at that point. If a harness is added only after an initial formal phase has already been observed, treat it as a labeled extension phase rather than retroactively part of the original prospective matrix.
