# Evidence

This directory stores neutral execution evidence that can support both software validation and research analysis. Evidence is kept outside the interpretive `research/` layer so users can inspect prior executions without adopting the study conclusions.

## Public run evidence

`public/` contains sanitized receipts and, where publishable, trajectories, workspace observations, and verifier output. OpenCode and Mini-SWE public trajectories can be inspected directly. The custom harness currently exposes black-box receipts and verifier history but not its private implementation or raw trajectory.

## Verifier revisions

`verifier-revisions/scenario1-v0.2.0/` preserves each verifier revision and the diff between revisions. The solver-visible task remains version `0.2.0`; verifier identity is recorded separately because verifier-only corrections do not require rerunning an agent whose workspace was produced without access to the hidden evaluator.

Revision 1 is the original collection-time verifier. Revision 2 corrected the forwarding-alias/canonical-reference overconstraint surfaced by Custom Attempt 1. Revision 3 adds explicit regression guards for two contract-visible edge cases without changing any recorded Scenario 1 outcome: concrete worker definitions remain forbidden even if renamed inside aggregate `$defs`, and registry drain/resume results must preserve the fields explicitly named by the task.
