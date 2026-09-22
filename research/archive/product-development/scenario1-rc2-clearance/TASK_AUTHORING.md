# Scenario 1 RC2 authoring note

Status: **0.2.0-rc1 task-clearance candidate**. This candidate supersedes RC1 after the first OpenCode clearance diagnostic showed that optional testing absorbed more route pressure than intended and the worker-only Python extraction was physically weaker than the focused R4 calibration.

## Design order

RC2 was designed primitive-first. The required interaction workload was fixed before the product wrapper:

- B1-like coordinated source work across worker state, registry/capacity, API/CLI, events, and examples;
- a substantial extraction/refactor class comparable to R4 without recreating the provider-class task;
- preservation-sensitive selective editing where it arises naturally;
- context stewardship across those operations;
- bounded testing scope so optional test generation cannot become the dominant workload.

The product wrapper was chosen afterward: worker draining/resume remains the coherent feature context, worker constructors move to `worker_events.py`, and worker JSON-Schema definitions move from the aggregate event schema to `worker-events.schema.json` while the aggregate remains the stable validation entry point.

Approximate patch sizes used to choose this candidate are **author-only calibration**, not solver or verifier requirements.

## Pressure-bearing spine

1. discover worker/event/schema/API/CLI ownership;
2. implement drain/resume state and distributed public behavior;
3. extract worker constructors while preserving compatibility and one shared event-ID sequence;
4. extract five worker event schemas from the repeated aggregate schema while preserving job/service definitions;
5. make aggregate validation resolve the sibling worker schema transparently;
6. update exactly the existing stale schema-location test and preserve the rest of repository validation;
7. converge across all surfaces without expanding into unrelated tests/docs.

## Verifier boundary

The verifier checks only contract-visible outcomes. It may check the explicitly required file/module/schema ownership, named public functions/events, compatibility behavior, named schema definitions, and the explicitly named validation test. It must not grade:

- patch size or line count;
- tool choice;
- number of edits/commands;
- use of JSON-aware tooling, shell, scripts, or structured edit helpers;
- helper-module layout;
- whether an edit command succeeds/fails;
- a particular external-reference spelling when another valid URI form resolves the required worker schema.

The workspace observer remains descriptive. The verifier normatively enforces only the explicit final-scope restriction under `tests/` and `docs/`.

## Focused-suite calibration

- **B1:** direct calibration for coordinated multi-file source work.
- **R4:** direct calibration for substantial extraction/integration class.
- **R1:** supporting analogue for selective editing among repeated structured regions; RC2 uses JSON Schema rather than TOML and should not be described as the same task.
- **V1:** supporting verification baseline for same-process behavioral evidence and tightly scoped test artifacts. RC2 does not require a REPL or any specific verification route.
