# Batchline

Batchline is a small local-first background-job processing library and control-plane model. It defines jobs and workers, renders job state for API and CLI consumers, emits lifecycle events, validates deployment configuration and event payloads, manages per-kind job policies, plans execution providers, and streams operational event archives.

The repository intentionally stays framework-light. There is no network service to start and no external database. Product behavior can be exercised entirely with local Python, YAML configuration, JSON fixtures, and JSON Schema validation.

## Common commands

```bash
make test
make validate-config
make validate-events
make validate-policies
make deployment-report
make check
```

All validation commands are expected to pass on the healthy repository baseline. `make deployment-report` is deliberately more detailed than the concise validation command and is useful for offline operational inspection.

## Repository map

- `src/batchline/jobs/` — job models, status handling, retry policy, in-memory service.
- `src/batchline/workers/` — worker runtime snapshots, registry, health evaluation.
- `src/batchline/api/` — serializer-facing public representations and stable error payloads.
- `src/batchline/cli/` — framework-independent command helpers and human-readable renderers.
- `src/batchline/events/` — lifecycle event envelopes, encoders, registry, schema validation.
- `src/batchline/policies/` — typed per-kind job policy catalog.
- `src/batchline/execution/` — local/container execution planning plus legacy remote compatibility.
- `src/batchline/operations/` — streaming JSONL operational archive helpers.
- `src/batchline/config/` — YAML loading, typed service configuration, schema validation, deployment validation, detailed reporting.
- `schemas/` — event and service configuration contracts.
- `tools/` — local validation, reporting, and fixture utilities.
- `examples/` — representative job and event payloads.

See `docs/concepts.md`, `docs/configuration.md`, `docs/job-policies.md`, and `docs/operations.md` for the product vocabulary.
