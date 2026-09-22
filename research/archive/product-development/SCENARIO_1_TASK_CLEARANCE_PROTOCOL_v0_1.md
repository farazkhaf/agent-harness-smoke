# Scenario 1 Task-Clearance Protocol — v0.1

Status: **active pre-freeze protocol**.

Purpose: establish that Scenario 1 is a coherent, correctly packaged task before any formal harness comparison begins. This stage is authoring/validation work. Its runs and notes are diagnostic inputs to task refinement, not canonical research findings.

## 1. Candidate identity

- Task: `agent-harness-smoke/batchline-worker-draining-event-extraction`
- Candidate version: `0.1.0-rc1`
- Anchor: Batchline `0.3-scenario1-seed`
- Candidate contract: first-class worker drain/resume lifecycle plus worker-event extraction and compatibility requirements.

The solver instruction, verifier, observer, anchor, oracle, and evaluation guide may still change during clearance. Material changes should advance the release-candidate revision rather than being hidden.

## 2. Clearance sequence

### C0 — local author checks

Already completed in the authoring environment:

- untouched/NOP simulation fails;
- author oracle passes all G1–G6 groups;
- repository-native checks pass;
- observer runs before verifier;
- verifier groups and observer output are preserved as distinct artifacts;
- targeted partial controls exercise the intended group boundaries.

These are authoring controls, not research observations.

### C1 — Harbor NOP on the author's machine

Run the unchanged candidate in the real Harbor path with no solver mutation.

Expected:

- binary reward `0`;
- named group vector consistent with the missing feature;
- workspace observer artifact is produced before verification;
- no evaluator/runtime error is mistaken for task failure.

If the result differs because of packaging/evaluator behavior, repair the task and rerun clearance. No evidence-preservation rule prevents such refinement at this stage.

### C2 — Harbor Oracle on the author's machine

Apply the author oracle through the real task environment and verifier path.

Expected:

- binary reward `1`;
- G1–G6 all pass;
- repository-native checks remain healthy;
- observer describes the final workspace without acting as a second verifier;
- named verifier-group artifact survives Harbor collection.

A failure here blocks solver clearance.

### C3 — one OpenCode diagnostic run

Run exactly one standard OpenCode 1.18.30 attempt with the normal matched model/provider configuration intended for this project.

This run is **not** O1, a canonical run, or formal comparative evidence. Give it a diagnostic identity such as `clearance-opencode-01`.

Do not protect its result from subsequent task changes. If it exposes an instruction, verifier, task-design, or packaging problem, fix the task and discard/repeat the diagnostic as necessary.

### C4 — joint task-coherence review

Review the OpenCode diagnostic using the scenario evaluation guide, but with a task-authoring purpose rather than a harness-performance purpose.

Questions:

- Did the instruction communicate the intended software target clearly?
- Did the solver discover the relevant runtime/event/module relationships without relying on unstated product requirements?
- Did the structural extraction requirement create the intended repository work rather than a trivial or artificial patch?
- Did any apparently valid shortcut expose an under-specified target or verifier gap?
- Did verifier groups diagnose the final implementation accurately?
- Did the shared event-helper/import boundary create a natural dependency-management pressure?
- If an import/cycle or validation failure occurred, was it a consequence of the intended change rather than task pathology?
- Did any requirement accidentally force the oracle's private helper layout or edit order?
- Were API/CLI/event/schema preservation clauses realistic and internally consistent?
- Did the task remain bounded enough for a first scenario?

Trajectory observations here may motivate refinement. They should not be published as comparative findings about OpenCode.

### C5 — refine and rerun controls if needed

If C3/C4 expose a material issue:

1. revise instruction/verifier/oracle/task packaging as appropriate;
2. advance the release-candidate revision if the solver-visible target or interpretation changes;
3. rerun NOP and Oracle Harbor controls;
4. run another diagnostic solver only if needed to validate the changed area.

The goal is task coherence, not preserving the first diagnostic run.

### C6 — task freeze

Freeze only when:

- Harbor NOP and Oracle are correct;
- the diagnostic solver route reveals no unresolved task-design defect;
- contract-to-verifier coverage remains complete;
- observer/verifier ordering is confirmed;
- task package and evaluation materials are internally consistent.

Then:

- promote to frozen task version (expected `0.1.0` if no RC revision is needed);
- record checksum;
- prohibit solver-facing interpretation changes under that version;
- begin research-protocol design.

## 3. What is explicitly out of scope during clearance

Do not yet:

- call solver attempts canonical research runs;
- build cross-harness rankings or findings;
- preserve a fixed repeat matrix for statistical interpretation;
- interpret OpenCode behavior as a stable harness property;
- choose a repeat count because of the diagnostic outcome;
- treat task-authoring corrections as post-hoc benchmark repair.

Task refinement before freeze is the purpose of this stage.

## 4. Research decisions deliberately deferred

After task freeze, decide prospectively:

- core harness set;
- whether OpenHands, Codex, or another harness is included in the primary matrix;
- repeat count per cell (two is currently a reasonable candidate; not fixed here);
- model/configuration matching;
- formal result-selection and invalidation rules;
- whether one attempt per cell receives deeper narrative treatment;
- publication/evidence-retention policy.
