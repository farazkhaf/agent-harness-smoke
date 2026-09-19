# Configuration

Batchline keeps base service declarations in `config/services.yaml` and environment policy in `config/environments/*.yaml`.

## Service catalog

A service entry defines the queue and local execution policy used by Batchline control-plane tooling:

- `queue`
- `concurrency`
- `timeout_seconds`
- `max_retries`
- `enabled`

The mapping key is the canonical service name. The raw YAML document is validated against `schemas/service-config.schema.json` before Batchline constructs typed `ServiceConfig` objects.

Environment files can override service settings and can declare required effective settings. Production validation checks the effective catalog against those requirements.

## Validation commands

`make validate-config` performs the concise production deployment check.

`make deployment-report` prints a detailed deterministic report containing each service's effective settings, whether a setting came from the base catalog or an environment override, applicable policy checks, diagnostics, and a final result. This report is intended for offline review and troubleshooting; normal validation remains concise.
