# Focused tasks

The `tasks/` directory contains five agent-agnostic Harbor task packages for the Batchline fixture repository:

- `batchline-submitted-by/` — B1 coordinated multi-file modification;
- `batchline-selective-retry-policies/` — R1 selective repeated edit;
- `batchline-remove-legacy-remote-provider/` — R2 large contiguous deletion;
- `batchline-quarantine-rate-limit-events/` — R3 large line-oriented inspection/filtering;
- `batchline-extract-legacy-remote-provider/` — R4 large contiguous move/module split.

Each task contains:

- `instruction.md` — solver-visible task contract;
- `task.toml` — Harbor task metadata and runtime limits;
- `environment/` — deterministic starting workspace and setup;
- `tests/` — verifier and workspace observer;
- `solution/` — author solution used for validation controls;
- `AUTHORING.md` — task rationale and verifier boundary;
- `AUTHOR_VALIDATION.md` — validation controls and formal status.

Task instructions do not prescribe a particular tool vocabulary or edit mechanism. Correctness is determined by the task verifier; workspace observations and trajectories are separate evidence.

Suite membership is declared in `../suites/batchline-focused/suite.toml`.
