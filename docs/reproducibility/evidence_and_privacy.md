# Evidence and privacy

Published evidence is limited to artifacts needed to inspect recorded outcomes and support the claims made from them. Raw Harbor stores, credentials, caches, host-specific paths, and private harness implementation details are excluded.

## Focused tasks

OpenCode and Mini-SWE focused runs include curated receipts, trajectories, workspace observations, and verifier output under `evidence/public/`. The custom-harness focused rows are published through normalized result and resource fields; its implementation and raw trajectories remain private.

## Scenario 1

OpenCode and Mini-SWE Scenario 1 attempts include ATIF trajectories, sanitized receipts, and verifier output under `evidence/public/scenario1/<harness>/attempt-<n>/`.

The custom-harness Scenario 1 attempts include sanitized receipts and verifier records. The custom harness implementation, prompts, tool schemas, adapters, and raw trajectory are private and are not required to reproduce the public route claims in the current study.

The original and current Scenario 1 verifiers are retained under `evidence/verifier-revisions/scenario1-v0.2.0/`. The original verifier documents the collection-time result; the current verifier is the canonical evaluator for the unchanged recorded workspaces.

## Evidence rule

A route-level claim should be supported by a published trajectory or other retained observable artifact. Result tables may include black-box outcome and telemetry fields for a private harness, but those fields do not by themselves support claims about its internal route.
