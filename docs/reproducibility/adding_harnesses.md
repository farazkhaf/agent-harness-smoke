# Adding a harness

Agent Harness Smoke tasks are agent-agnostic. New harnesses can be added without copying or modifying task packages.

## External Harbor agent

Use an external profile when the agent is already importable by the Harbor host process. The agent may receive a model from the suite or own its provider/model configuration itself.

```toml
[[profiles]]
id = "my-agent"
execution = "external"
agent = "my_package.harbor_adapter:MyAgent"
# model = "provider/model"  # optional
```

`runtime/scripts/run-suite.ps1` dispatches this profile through `run-external.ps1`. No runtime image or task binding is required.

## Reusable preinstalled runtime

Use a preinstalled profile when the harness should be installed once into a reusable image and bound to many canonical tasks.

A preinstalled integration has three parts:

1. a version-pinned runtime image, normally under `runtime/images/<agent>/`;
2. a Harbor agent wrapper/import path that verifies and uses the preinstalled harness;
3. a runtime profile that names the wrapper and image.

Example profile shape:

```yaml
schema_version: "0.1"
id: my-agent-1.2.3
agent: my-agent
integration: my_package.preinstalled:PreinstalledMyAgent
mode: preinstalled
version: "1.2.3"
image: harness-smoke/my-agent:1.2.3
image_digest: null
```

A suite then references the runtime profile:

```toml
[[profiles]]
id = "my-agent-1.2.3"
execution = "preinstalled"
runtime_profile = "runtime/profiles/my-agent-1.2.3.yaml"
model = "provider/model"
```

`runtime/bind_task.py` creates a temporary bound task by changing only the task Dockerfile's `HARNESS_SMOKE_BASE_IMAGE` default and recording binding metadata. Repository setup remains owned by the canonical task. The resolved task is disposable; agent-specific task copies are not maintained.

The included Mini-SWE and OpenCode images, wrappers, and profiles are reference implementations of this pattern.

## Normalized telemetry boundary

Harness-native usage formats are outside the public collector contract. For token-comparable reporting, an integration should expose normalized ATIF usage with non-reasoning completion/output tokens in `final_metrics.total_completion_tokens` and reasoning tokens separately in `final_metrics.extra.total_reasoning_tokens` when available. The public reporter consumes that normalized boundary and does not parse private/native harness metrics.
