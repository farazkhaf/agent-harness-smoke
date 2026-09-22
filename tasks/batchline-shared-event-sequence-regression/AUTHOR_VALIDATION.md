# Author validation — batchline-shared-event-sequence-regression 0.1.0

Expected author checks before collection:

- NOP: existing repository tests pass, but the hidden verifier returns reward 0 because the shared sequence and required regression test are absent.
- Oracle: `solution/solve.sh` changes only the two contracted paths, the submitted regression test catches the baseline bug, the non-1 counter robustness check passes, all repository tests pass, and the hidden verifier returns reward 1.
- Workspace observer runs before the verifier and remains descriptive.

This task is an additive focused-suite task. It does not require rerunning previously completed focused-task cells.

Canonical focused-task status: accepted as V1 after one passing run each from OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1. No solver-facing instruction, verifier, environment, or oracle content changed between the executed RC1 package and the promoted 0.1.0 task; only release metadata/documentation changed.
