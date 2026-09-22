# Provenance

## Project identity

Agent Harness Smoke uses the Harbor task namespace `agent-harness-smoke`. Version 0.2.1 contains six focused task identities plus Scenario 1, `agent-harness-smoke/batchline-worker-draining-event-extraction`.

The focused `accepted-18` checkpoint contains one recorded run for each of six tasks across OpenCode, Mini-SWE-Agent, and the custom harness. Scenario 1 contains two recorded runs per harness configuration.

## Execution software

All recorded focused and Scenario 1 executions in this release use Harbor 0.22.0 with Docker-backed task environments. Harbor orchestrates task environments, agent execution, trial records, observers/verifiers, and result collection.

The recorded public harnesses are OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6. The model is GLM-5.3-Flash served through Fireworks AI. The private custom harness is identified by its release-local snapshot/profile name and is not redistributed. See `docs/provenance/software_attribution.md` for external software references.

## Reasoning configuration

The bundled OpenCode and Mini-SWE focused profiles omit `reasoning_effort`, so GLM-5.3-Flash uses its documented default. Historical custom-harness focused runs explicitly used `high`; focused custom/public differences are therefore not interpreted as harness-only effects. Scenario 1 uses matched effective `max` reasoning.

## Telemetry normalization

Published normalized results distinguish non-reasoning completion/output tokens from reasoning tokens when the underlying execution record exposes that split. Harness-native usage formats are not part of the public collector contract; integrations normalize usage at the ATIF/reporting boundary. The retained custom-harness output/reasoning split is derived from the preserved native usage records for the published runs. Provider-reported cost is retained independently of token normalization.

## Scenario 1 evaluator identity

Scenario 1 remains solver-visible task version `0.2.0`. Recorded results in this release use verifier revision `r3`; the collection-time verifier is retained as evaluator provenance under `evidence/verifier-revisions/scenario1-v0.2.0/`. The adjudication that motivates retaining both versions is documented once in `docs/provenance/scenario1_verifier_history.md`.

## Authorship

Agent Harness Smoke v0.2.1 is authored by Faraz Ul Khaf. `CITATION.cff`, `VERSION`, and `CHANGELOG.md` provide release identity and continuity.
