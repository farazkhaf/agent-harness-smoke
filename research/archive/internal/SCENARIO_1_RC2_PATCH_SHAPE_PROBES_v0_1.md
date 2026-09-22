# Scenario 1 RC2 Patch-Shape Probes — v0.1

Status: internal task-designer note. Not solver-facing and not research evidence.

## Design order

The operation workload is primary. Product semantics are accepted only after a candidate patch shape is shown to instantiate the intended workspace pressures. Approximate line counts and operation sizes below are authoring calibration only; they must not become hidden verifier criteria.

## Required pressure envelope

Primary targets carried from the focused suite:

- B1-like coordinated source work across multiple runtime/public surfaces.
- R4-like substantial extraction/module-split/refactor pressure with preservation of unrelated implementation.
- Prefer, but do not force, preservation-sensitive selective editing where the repository naturally supplies repeated/near-repeated structure.
- Scenario composition should create context-stewardship pressure between these operations without relying primarily on semantic ambiguity, self-authored tests, or induced tool failures.

## Candidate A — split every event constructor domain

Shape: move job, worker, and service constructor families out of `events/encoder.py`; leave `encoder.py` as a compatibility facade.

Measured shape from the throwaway probe:

- roughly 226 lines removed from the original encoder;
- new modules around 45 lines (job), 139 lines (worker), and 31 lines (service);
- overall product-surface diff roughly +377 / -229 across 13 paths once the worker lifecycle work is included.

Assessment: physically substantial, but too close to replaying R4. It can also collapse into a straightforward whole-file rewrite of `encoder.py` plus three new files. Keep only as a fallback/reference candidate.

## Candidate B — RC1 worker code extraction + dedicated worker JSON Schema extraction

Shape:

1. Keep the first-class worker drain/resume lifecycle and coordinated runtime/API/CLI changes.
2. Keep the worker-event Python extraction to `events/worker_events.py` with legacy imports preserved through `events.encoder`.
3. Extract all worker event schema definitions from the large monolithic `schemas/events.schema.json` into `schemas/worker-events.schema.json`.
4. Keep `events.schema.json` as the aggregate public schema, but have its worker variants reference the dedicated worker schema.
5. Update validation so the aggregate schema resolves the sibling worker schema transparently and registry/schema parity continues to include all event types.
6. Update the one existing schema-location test whose assumption is now stale; do not require free-form new tests.

Measured patch shape:

- RC1 baseline itself: about +303 / -121 across 11 paths.
- RC2 incremental schema split versus RC1: +363 / -318 across only 4 paths:
  - `schemas/events.schema.json`: +5 / -312;
  - new `schemas/worker-events.schema.json`: +339;
  - `src/batchline/events/validation.py`: +14 / -3;
  - `tests/events/test_validation.py`: +5 / -3.
- In the RC1 schema, the five worker definitions occupy one contiguous region of roughly 307 lines (around lines 500–806 of the 914-line schema).
- Five worker variants among the aggregate root references are selectively rewired; job/service variants remain in place.
- The separate Python worker-constructor extraction remains roughly a 95-line old-module region with a ~139-line destination module.
- Combined anchor-to-candidate product-surface diff is roughly +601 / -374 across 14 paths.

Validation result: repository `make check` passes (55 tests plus config/event/policy validation).

Pressure assessment:

- B1 coordination: retained across worker model, registry, serializer, CLI rendering/commands, event registry/example.
- Structural extraction: now substantial in two different artifact types rather than only a small Python move.
- Selective/preservation-sensitive editing: naturally present in the large repeated JSON Schema; only worker definitions/references move while job/service definitions must remain equivalent.
- Route diversity is plausible without requiring errors: a solver may use structured text edits, whole-file rewrite, JSON-aware scripting, shell extraction, or mixed inspection/editing.
- Does not require adding a new product feature solely for size.

Assessment: preferred candidate.

## Candidate C — split the existing event encoder tests by domain

Shape: retain RC1 and replace the 76-line `tests/events/test_encoder.py` with explicit job/worker/service test files.

Measured shape:

- 76-line contiguous deletion of the old test file;
- three replacement test files;
- overall diff roughly +351 / -197 across 15 product/test paths.

Assessment: provides more deletion/move work, but makes test organization a primary primitive despite no focused calibration for that surface and risks recreating the RC1 problem where testing dominates route variance. Reject as a primary pressure source. A small, explicit stale-test update is acceptable when naturally required by Candidate B.

## Product gate for Candidate B

Candidate B passes the product-coherence gate without driving the design:

- Worker events are already becoming a first-class event family in Python because the scenario adds drain/resume lifecycle semantics.
- The event schema is already large (847 lines at anchor, 914 lines after the RC1 lifecycle additions), and all worker event definitions are contiguous/repeated variants.
- Mirroring worker-event ownership in schema as well as Python is a credible maintenance split rather than an unrelated benchmark artifact.
- The public aggregate event schema can remain the stable entry point, preserving existing callers while validation resolves the dedicated worker schema.
- An existing repository test explicitly assumes `WorkerRateLimitedEvent` lives in the monolithic schema, so one exact test maintenance change is naturally required. No open-ended test generation is needed.

## Verifier boundary later

The eventual solver instruction may explicitly require the named module/schema ownership and compatibility behavior. The verifier may check those stated outcomes. It must not check authoring calibration such as line counts, number of edit calls, use of shell versus edit tools, or any preferred extraction procedure.

Before RC2 freeze, verifier checks that inspect source/module/schema location must be audited one-by-one against the final solver contract so no unstated keyword/source-form assumption is introduced.
