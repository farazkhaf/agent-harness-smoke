# Scenario 1 Formal Run Protocol — deferred draft

Status: **inactive until task clearance is complete**.

This file is intentionally not a binding research protocol yet. Scenario 1 is still in task-authoring/clearance. The task may change after author-runtime controls or after review of one diagnostic OpenCode trajectory. Those changes are normal task refinement and do not create a research-evidence obligation.

The pre-clearance research draft that previously fixed a 3×3 matrix is preserved for history at:

`docs/archive/SCENARIO_1_FORMAL_RUN_PROTOCOL_v0_1_PRE_CLEARANCE_DRAFT.md`

## When to write the real formal protocol

Only after all task-clearance gates pass:

1. Harbor NOP behaves as expected.
2. Harbor Oracle passes unchanged.
3. Observer and named verifier-group artifacts survive the real Harbor path.
4. One standard OpenCode run is executed specifically as a **task-design diagnostic**, not as comparative evidence.
5. Its final state and trajectory are reviewed for task coherence, hidden ambiguity, accidental implementation prescription, verifier gaps, shortcut paths, and unexpected interaction pressures.
6. Any required task/verifier/instruction changes are made and the clearance controls are rerun.
7. The task is then frozen/versioned and checksummed.

After that point, define prospectively:

- the formal harness set;
- whether OpenHands, Codex, or another harness joins the comparison;
- model/provider/configuration matching rules;
- repeat count per cell (two runs is a live candidate, not yet fixed);
- invalidation/replacement rules;
- canonical/narrative-run convention if one is still useful;
- public/private evidence boundaries.

If a new harness is added only after the initial formal matrix has been observed, report it as a later extension phase rather than implying it was part of the original prospective matrix.
