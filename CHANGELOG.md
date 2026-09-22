# Changelog

## v0.2.0 — 2026-09-21

Focused-suite expansion.

- Adds V1, `batchline-shared-event-sequence-regression`, for same-process behavioral verification with a constrained regression artifact.
- Expands the canonical checkpoint from 15 to 18 rows without rerunning B1/R1-R4.
- Adds OpenCode and Mini-SWE V1 trajectory/observer/verifier evidence and one normalized `custom-harness` snapshot-1 row.
- Preserves the original `accepted-15/` v0.1.0 matrix unchanged and adds `accepted-18/` for v0.2.0.
- Adds explicit V1 promotion provenance: the executed `0.1.0-rc1` task and published `0.1.0` task have identical solver-visible instruction, verifier logic, observer logic, environment, and solution content.
- Extends the reporter with generic `inference_count` compatibility and public alias/redaction controls for private-harness normalization.

## v0.1.0 — 2026-09-19

Initial Agent Harness Smoke release.

- Adds five Harbor-native Batchline tasks covering coordinated multi-file modification, selective repeated editing, large contiguous deletion, large line-oriented inspection/filtering, and module extraction.
- Records the canonical 15-cell result matrix across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
- Includes OpenCode and Mini-SWE run receipts, trajectories, workspace observations, and verifier output.
- Separates verifier correctness, workspace observation, trajectory evidence, and runtime/resource telemetry.
- Establishes the `agent-harness-smoke/*` Harbor task namespace.

## Scenario 1 task v0.2.0 — 2026-09-21

- Publishes `batchline-worker-draining-event-extraction` at task version `0.2.0` after clean Harbor NOP/oracle controls and a matched OpenCode pre-release diagnostic.
- Preserves the validated instruction, verifier, and seed repository unchanged while adding descriptive observer instrumentation and release documentation.
- Keeps the dedicated worker-event JSON-Schema extraction, aggregate-schema compatibility, bounded existing-test maintenance, and worker Python extraction selected during RC2 design.
- Adds observer schema 0.2 so untracked text-file additions are reported separately from tracked `git diff --numstat` lines while standard Git ignores exclude caches/build products.
- Added the Scenario 1 comparison suite with two runs per public harness and a Scenario 1 runner.
- Scenario suites now default to `results/batchline-scenarios/<suite-id>/<timestamp>` when `-OutputRoot` is omitted.
- Compact Markdown result tables now display and sort repeated-run attempts explicitly.

## Scenario 1 repeated-run evidence — 2026-09-22 (comparison workspace)

- Adds completed Scenario 1 two-run cells for OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6. OpenCode passes both runs; Mini-SWE passes one run and one run reaches the declared 600-second agent timeout with a remaining G1 lifecycle defect.
- Adds public ATIF trajectories, sanitized run receipts, verifier output, and normalized repeated-run output for both public cells.
- Rewrites the Scenario 1 evaluation guide as reproducible run-analysis guidance organized around inspection primitives, transformation routes, recovery cause, validation milestones, and context stewardship.
- Extends the Scenario 1 findings (now under `research/scenario-1/FINDINGS.md`) with step-level analysis of the OpenCode and Mini-SWE repeated-run cells.
- Replaces development-stage Scenario 1 analysis notes with the public run-evaluation guide and archives earlier task-development records.
- Keeps the executable Scenario 1 task surface unchanged.

## Scenario 1 verifier revision 2 — 2026-09-22

- Keeps solver-visible Scenario 1 task version `0.2.0` and all six recorded agent executions unchanged.
- Archives verifier revision 1 and its original outcomes.
- Corrects G5 to accept pure local forwarding aliases to `worker-events.schema.json` while continuing to reject concrete worker schema assertions in the aggregate schema.
- Removes smaller non-contract assumptions around registry object identity, a specific legacy-heartbeat fixture shape, and standalone worker-event validation without a reference registry.
- Reconstructs Custom Attempt 1 from its trajectory, reproduces the original G5-only revision-1 failure, and verifies the identical workspace as G1-G6 pass under revision 2.
- Preserves Mini-SWE Attempt 1 as a valid G1 failure and 600-second agent-timeout outcome.
- Adds canonical verifier-r2 combined results for OpenCode, Mini-SWE, and the custom harness while retaining verifier-r1 history.

## Research/product separation and verifier revision 3 — 2026-09-22

- Separates active product documentation (`docs/`), neutral run evidence (`evidence/` and `results/`), and interpretive study material (`research/`) while keeping one shared source tree.
- Adds `research/STUDY_OBJECTIVE.md` and `research/METHODS.md`; moves Scenario 1 interpretive findings under `research/scenario-1/`.
- Defines a core release artifact that excludes `research/` and a study snapshot that includes the full research layer; both use the same tasks/results/evidence.
- Preserves custom-harness Scenario 1 data at the black-box outcome/telemetry level and defers any sanitized trajectory format until route-level custom claims require it.
- Adds verifier revision 3 without changing solver-visible task version `0.2.0` or any recorded Scenario 1 outcome. r3 rejects renamed concrete worker schemas retained in aggregate `$defs` and explicitly checks registry preservation fields, while allowing direct external worker `$ref` entries with harmless siblings such as `type: object`.
