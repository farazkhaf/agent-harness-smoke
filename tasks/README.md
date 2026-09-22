# Focused tasks

The `tasks/` directory contains six locked agent-agnostic Harbor task packages for the Batchline fixture repository:

- `batchline-submitted-by/` — B1 coordinated multi-file modification;
- `batchline-selective-retry-policies/` — R1 selective repeated edit;
- `batchline-remove-legacy-remote-provider/` — R2 large contiguous deletion;
- `batchline-quarantine-rate-limit-events/` — R3 large line-oriented inspection/filtering;
- `batchline-extract-legacy-remote-provider/` — R4 large contiguous move/module split;
- `batchline-shared-event-sequence-regression/` — V1 same-process behavioral verification with a constrained regression artifact.

Each locked focused task contains:

- `instruction.md` — solver-visible task contract;
- `task.toml` — Harbor task metadata and runtime limits;
- `environment/` — deterministic starting workspace and setup;
- `tests/` — verifier and workspace observer;
- `solution/` — author solution used for validation controls;
- `AUTHORING.md` — task rationale and verifier boundary;
- `AUTHOR_VALIDATION.md` — validation controls and formal status.

Task instructions do not prescribe a particular tool vocabulary or edit mechanism. Correctness is determined by the task verifier; workspace observations and trajectories are separate evidence.

Locked public-suite membership is in `../suites/batchline-focused/suite.toml`. The historical one-task V1 development suite is retained under `../suites/archive/` for provenance; adding V1 did not require rerunning B1/R1-R4.

## Scenario task

`batchline-worker-draining-event-extraction/` is the Scenario 1 task at `0.2.0`. It is not a seventh focused task and is not included in the focused `accepted-18` matrix. Development records are archived outside the task directory; `EVALUATION_GUIDE.md` defines the public run-analysis procedure.
