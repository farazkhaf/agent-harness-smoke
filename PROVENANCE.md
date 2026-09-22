# Provenance

## Project identity

The project title is Agent Harness Smoke and the Harbor task namespace is `agent-harness-smoke`. Version 0.2.0 publishes six focused task identities plus Scenario 1 `agent-harness-smoke/batchline-worker-draining-event-extraction`.

The focused `accepted-18` matrix contains one canonical run for each of six task/harness cells across OpenCode, Mini-SWE, and the custom harness. The original 15-row checkpoint remains preserved.

## Reasoning configuration

The public OpenCode and Mini-SWE focused profiles omit `reasoning_effort`, so GLM-5.3-Flash uses its documented default `max`. Historical custom-harness focused runs explicitly used `high`; therefore focused custom/public differences are not treated as harness-only effects. Scenario 1 uses matched effective `max` reasoning.

## Scenario 1 verifier identity

Scenario 1 keeps solver-visible task version `0.2.0`. The instruction, seed repository, Dockerfile, task metadata, observer, test wrapper, and oracle solution used for the recorded executions are unchanged by later verifier maintenance. Verifier identity is recorded independently.

- **r1** — original collection-time verifier.
- **r2** — contract correction accepting pure forwarding aliases and removing several non-contract implementation assumptions. Custom Attempt 1 changes from G5-only fail to pass when the identical workspace is re-evaluated.
- **r3** — regression hardening only. It detects concrete worker schemas retained under renamed aggregate `$defs` entries and explicitly checks preservation fields on registry drain/resume returns/stored snapshots. Direct external worker `$ref` entries may still carry harmless siblings such as `type: object`. No recorded Scenario 1 outcome changes from r2.

The revisions and diffs are retained under `evidence/verifier-revisions/scenario1-v0.2.0/`.

## Custom Attempt 1 adjudication

Custom Attempt 1 originally failed G5 because r1 treated any same-named local worker `$defs` entry as retained concrete ownership and required one canonical direct-reference layout. The workspace instead used pure local forwarding aliases whose concrete worker definitions lived in `worker-events.schema.json`. Because the solver-visible contract required concrete ownership to move but did not prohibit forwarding aliases, r2 corrected the evaluator rather than changing the task instruction. The original r1 result remains historical evidence; r2+ is the canonical contract interpretation. No agent rerun was used to produce that change.

## Authorship

Agent Harness Smoke v0.2.0 is authored by Faraz Ul Khaf. `CITATION.cff`, `VERSION`, and `CHANGELOG.md` provide release continuity.
