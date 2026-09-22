# Task design — agent-harness-smoke/batchline-shared-event-sequence-regression 0.1.0

## Purpose

This focused task isolates verification of a process-global invariant. The seed makes lifecycle-event ID counters independent by prefix while leaving the existing repository tests green. The required fix is intentionally small; the interaction pressure is in constructing and validating a regression that must observe multiple event families inside one Python process.

## Interaction focus

Primary interaction family: same-process behavioral verification with a constrained regression artifact.

Plausible valid routes include the required regression artifact itself, a persistent Python/IPython session, a one-shot Python program or here-document, a reusable scratch probe, direct targeted pytest execution, or counterfactual/negative-control validation. The task does not require or score any particular route or treat persistent execution as preferable.

## Why the test contract is explicit

Open-ended test generation would add model-policy variance unrelated to the focused interaction. The task therefore names one test file, one test function, the families it must exercise, the monotonic numeric property, and the two-path edit scope.

## Starting state

`src/batchline/events/encoder.py` uses an independent `itertools.count(1)` for each event-ID prefix. Existing constructor/schema tests still pass because they validate event shape independently rather than cross-family process-global sequencing.

## Contract boundary

The verifier checks only stated requirements:

- only `encoder.py` and the named regression test may change;
- the named regression test passes on the submitted solution;
- job, worker, and service/config events share one numeric sequence in a single process;
- the submitted test fails against the seeded per-prefix baseline;
- the submitted test does not depend on the correct global counter starting at 1;
- the existing repository tests remain healthy.

The verifier does not require a REPL, a scratch script, a particular shell command, a particular internal counter variable name, or a particular source-edit mechanism.
