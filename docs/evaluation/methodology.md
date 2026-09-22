# Methodology

## Evaluation model

Each harness is treated as a black box that receives the same task instruction and reproducible starting workspace through Harbor. Evaluation uses the final externally observable state together with task-defined verification.

Four evidence layers are kept separate:

1. Verifier — contract correctness. Checks the behavior and preservation requirements stated by the task.
2. Workspace observer — final-state description. Records changed paths and coarse diff statistics without deciding correctness unless the task explicitly constrains scope.
3. Compact report — cross-harness comparison surface. Records task and harness identity, reward, model-call count when available, token/cache totals, cost, and timing.
4. Trajectory — interaction-route evidence. Used to inspect how a run proceeded and to diagnose unusual outcomes; it is not part of the reward.

This separation prevents edit strategy, Git shape, or incidental extra files from becoming hidden correctness criteria.

## Focused-task selection

A focused task is intended to create a distinct workspace interaction requirement while keeping semantic ambiguity modest. The design question is:

> If the model already knew exactly what final change was required, what would the harness still have to do differently from the other tasks?

The Batchline suite therefore covers coordinated propagation, selective repeated editing, substantial deletion, large line-oriented inspection, and substantial move/module splitting.

## Controlled comparison

The public harness cells use the same underlying model family and the same canonical task packages. Harness-native provider identifiers and tool vocabularies are retained. A harness may use shell commands, structured file tools, scripts, or mixed strategies; the verifier does not prescribe one mechanism.

Comparisons are grouped by logical task ID and task version. Runtime-specific checksums and temporary binding paths are not used as cross-harness task identities.

## Resource telemetry

`input_tokens` is cumulative end-to-end prompt/context usage reported by the Harbor/provider integration. Cached tokens are a subset when available; uncached input is derived only when both totals are present. Output tokens, model-call count, provider-reported cost, agent execution time, and total elapsed time are reported when available.

These fields describe a particular run route. They should not be interpreted as pure reasoning efficiency. Elapsed time can include environment setup, test execution, validation depth, recovery work, and runtime overhead. The suite does not compute an aggregate efficiency score.

## Sampling and interpretation

Focused checkpoints and scenario cells are retained as observed executions rather than population estimates. Scenario 1 currently uses two repetitions per harness. Those repetitions can document route recurrence, route variation, and concrete failure/recovery episodes, but they are not used to rank harness products or estimate stable success probabilities.

The reusable evaluator therefore reports correctness and telemetry without computing a composite harness score. Research-level interpretation is kept under `research/`.
