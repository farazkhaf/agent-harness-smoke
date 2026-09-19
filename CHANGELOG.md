# Changelog

## v0.1.0 — 2026-09-19

Initial Agent Harness Smoke release.

- Adds five Harbor-native Batchline tasks covering coordinated multi-file modification, selective repeated editing, large contiguous deletion, large line-oriented inspection/filtering, and module extraction.
- Records the canonical 15-cell result matrix across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
- Includes OpenCode and Mini-SWE run receipts, trajectories, workspace observations, and verifier output.
- Separates verifier correctness, workspace observation, trajectory evidence, and runtime/resource telemetry.
- Establishes the `agent-harness-smoke/*` Harbor task namespace.
