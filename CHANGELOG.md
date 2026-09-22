# Changelog

## v0.2.1 — 2026-09-22

- Supersedes v0.2.0 as the canonical public source/archive release.
- Uses the active focused and Scenario 1 suite/result surfaces together with the active research, reproducibility, and software-provenance documentation.
- Corrects token normalization for the eight retained custom-harness executions by separating non-reasoning output from reasoning tokens using retained native usage records.
- Narrows the public release to active software, evidence, documentation, and research artifacts.
- Does not change solver-visible task versions, recorded agent executions, workspaces, provider-reported cost, or current-verifier outcomes.

## v0.2.0 — 2026-09-22

- Adds V1 `batchline-shared-event-sequence-regression`, bringing the focused suite to six tasks and the recorded focused checkpoint to 18 accepted runs.
- Adds Scenario 1 `batchline-worker-draining-event-extraction` with two recorded executions each for OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and the custom harness.
- Adds reusable suite execution for both preinstalled runtime profiles and external Harbor agent import paths.
- Adds Scenario 1 trajectory analysis for the published OpenCode and Mini-SWE trajectories.
- Corrects the Scenario 1 verifier so schema ownership is not tied to one canonical forwarding/reference layout; the collection-time verifier is retained for provenance and no agent execution is rerun.
- Keeps the 18-run focused checkpoint as the active focused result set.
- Adds explicit software/citation provenance for Harbor 0.22.0, Docker-backed execution, OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, GLM-5.3-Flash, and Fireworks AI.

## v0.1.0 — 2026-09-19

- Adds five Harbor-native Batchline tasks covering coordinated multi-file modification, selective repeated editing, substantial contiguous deletion, large line-oriented inspection/filtering, and module extraction.
- Records the initial 15 focused executions across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
- Establishes separate verifier correctness, workspace observation, trajectory evidence, and runtime/resource telemetry.
- Establishes the `agent-harness-smoke/*` Harbor task namespace.
