# Evidence

This directory contains curated execution artifacts associated with the recorded results.

`public/` contains published run receipts and, where available, trajectories, workspace observations, and verifier output. OpenCode and Mini-SWE trajectories are included. Custom-harness raw trajectories and implementation details remain private.

`verifier-revisions/scenario1-v0.2.0/` contains the original collection-time Scenario 1 verifier (`v1`), the current verifier (`v3`), their direct diff, and regression evidence. The solver-visible Scenario 1 task remains version `0.2.0`; verifier identity is tracked separately because a verifier-only correction does not alter the workspace an agent produced.
