# Task design

The focused suite targets workspace-interaction primitives rather than semantic or algorithmic difficulty. Each task is deterministic, self-contained, and designed to be understandable without network access beyond the harness/model integration.

## Task families

| Family | Task | Interaction target |
|---|---|---|
| B1 | submitted-by | coordinated change across model, service, API, and CLI surfaces |
| R1 | selective retry policies | repeated selective edits among many similar entries |
| R2 | remove legacy provider | substantial contiguous deletion with contract-preserving cleanup |
| R3 | quarantine events | scan/filter a multi-megabyte line-oriented archive and emit a derived artifact |
| R4 | extract legacy provider | substantial contiguous move into a new module while preserving registry behavior |

## Authoring rules

- The task instruction states the observable product contract rather than a preferred tool sequence.
- Verifiers check stated behavior, required preservation, protected inputs, parsing/loading, and structural conditions that are necessary to the task contract.
- Exact oracle diffs, exact line numbers, exact tool usage, and formatting preferences are not verifier requirements unless explicitly stated by the task.
- Workspace observations may record additional changed paths without turning them into failures unless the task constrains those paths.
- Focused tasks use modest semantics so interaction-route differences can be inspected without making hidden product reasoning the main source of difficulty.

Task-specific design and control notes are included in each task package.
