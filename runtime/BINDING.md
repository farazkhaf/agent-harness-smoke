# Runtime binding

Canonical tasks are agent-agnostic. A reusable preinstalled harness is installed once in a version-pinned runtime image and bound to a task only for the duration of a run.

## Binding contract

- task packages own repository content and setup requirements;
- runtime profiles identify the preinstalled agent image and Harbor integration;
- `runtime/bind_task.py` creates an ephemeral task copy and changes only the Dockerfile's `HARNESS_SMOKE_BASE_IMAGE` default;
- binding metadata is written to `.harness-smoke-binding.json`;
- agent-specific task copies are not maintained.

Canonical task Dockerfiles follow this pattern:

```dockerfile
ARG HARNESS_SMOKE_BASE_IMAGE=<standalone default>
FROM ${HARNESS_SMOKE_BASE_IMAGE}

WORKDIR /app
COPY repo/ /app/
COPY setup/ /tmp/harness-smoke-repo-setup/
RUN /tmp/harness-smoke-repo-setup/setup.sh
```

The included Mini-SWE and OpenCode integrations demonstrate the pattern. Additional cached/preinstalled agents can add their own image, wrapper, and runtime profile and then use the same binder and suite runner. External Harbor agents can bypass image binding entirely; see `docs/reproducibility/adding_harnesses.md`.

## Examples

```powershell
.\runtime\scripts\run-mini-swe-preinstalled.ps1 `
  -TaskPath "tasks\batchline-submitted-by"

.\runtime\scripts\run-opencode-preinstalled.ps1 `
  -TaskPath "tasks\batchline-submitted-by"
```

Use `-KeepResolvedTask` only when inspecting the generated temporary binding.
