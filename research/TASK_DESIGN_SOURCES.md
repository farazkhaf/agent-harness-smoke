# Task-design sources

Task construction is part of the research method. The canonical authoring records remain with the task packages so that the same files are useful to both task maintainers and researchers.

## General design rules

- [`../docs/evaluation/task_design.md`](../docs/evaluation/task_design.md) — task and verifier boundary.
- [`../docs/evaluation/methodology.md`](../docs/evaluation/methodology.md) — evidence layers and run telemetry.

## Focused tasks

Each focused task contains an `AUTHORING.md` rationale and an `AUTHOR_VALIDATION.md` control record:

- [`batchline-submitted-by`](../tasks/batchline-submitted-by/AUTHORING.md)
- [`batchline-selective-retry-policies`](../tasks/batchline-selective-retry-policies/AUTHORING.md)
- [`batchline-remove-legacy-remote-provider`](../tasks/batchline-remove-legacy-remote-provider/AUTHORING.md)
- [`batchline-quarantine-rate-limit-events`](../tasks/batchline-quarantine-rate-limit-events/AUTHORING.md)
- [`batchline-extract-legacy-remote-provider`](../tasks/batchline-extract-legacy-remote-provider/AUTHORING.md)
- [`batchline-shared-event-sequence-regression`](../tasks/batchline-shared-event-sequence-regression/AUTHORING.md)

The corresponding `AUTHOR_VALIDATION.md` file in each task records its validation controls.

## Scenario 1

- [`../tasks/batchline-worker-draining-event-extraction/AUTHORING.md`](../tasks/batchline-worker-draining-event-extraction/AUTHORING.md) — scenario construction and verifier boundary.
- [`../tasks/batchline-worker-draining-event-extraction/AUTHOR_VALIDATION.md`](../tasks/batchline-worker-draining-event-extraction/AUTHOR_VALIDATION.md) — current validation controls.
- [`../tasks/batchline-worker-draining-event-extraction/EVALUATION_GUIDE.md`](../tasks/batchline-worker-draining-event-extraction/EVALUATION_GUIDE.md) — trajectory-analysis procedure.

These are the approved design sources for the study. Historical candidates and rejected designs are not used as active methodology.
