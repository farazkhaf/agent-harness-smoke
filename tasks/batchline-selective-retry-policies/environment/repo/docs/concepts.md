# Batchline concepts

## Jobs

A job is a unit of background work identified by an opaque ID and a stable `kind`. Jobs are submitted to a named queue and move through a deliberately small lifecycle: queued, running, succeeded, failed, or canceled. The domain model does not implement scheduling or distributed locking; Batchline only models the state exposed by surrounding systems.

Jobs also track the current attempt number, the maximum number of attempts, timestamps, and optional result or error metadata. Retry decisions are separated into `jobs.retry` so status handling remains easy to inspect.

## Workers

A worker describes an execution process attached to one service and one queue. Deployment configuration determines concurrency, timeouts, retry limits, and whether a worker is enabled. The in-memory registry records current worker snapshots and provides simple lookup/filtering operations.

## API and CLI surfaces

Batchline has no HTTP server. The `api.serializers` package represents the stable dictionaries that an API layer could expose. CLI modules likewise contain rendering and command helpers rather than a framework-specific command parser. This keeps the repository focused on repository-editing behavior instead of framework conventions.

## Events

Lifecycle events use a common envelope and typed payloads. The event schema is intentionally centralized in `schemas/events.schema.json`, while `events.encoder` contains ordinary constructors for common job and worker events. The schema can therefore be validated without running a service.

## Configuration

`config/services.yaml` contains the base worker/service declarations. Environment files under `config/environments/` provide deployment expectations and optional overrides. `tools/validate_deploy.py` checks the effective configuration for a chosen environment and emits line-oriented diagnostics suitable for humans or automation.
