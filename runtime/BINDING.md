# Runtime binding

The public harness images contain the expensive harness installation and are reused across canonical tasks. Each task remains agent-agnostic and owns its repository/setup requirements.

## Invariants

- Mini-SWE/OpenCode are installed once in version-pinned runtime images.
- Thin Harbor wrappers verify/use those installations rather than reinstalling the harness for every task.
- Canonical Harbor tasks remain standalone task packages.
- Repository preparation lives in `environment/setup/setup.sh`.
- `runtime/bind_task.py` creates an ephemeral bound task by changing only the Dockerfile's `HARNESS_SMOKE_BASE_IMAGE` default and adding binding metadata.
- Agent-specific task copies are not maintained in the repository.

## Canonical environment convention

```dockerfile
ARG HARNESS_SMOKE_BASE_IMAGE=<standalone default>
FROM ${HARNESS_SMOKE_BASE_IMAGE}

WORKDIR /app
COPY repo/ /app/
COPY setup/ /tmp/harness-smoke-repo-setup/
RUN /tmp/harness-smoke-repo-setup/setup.sh
```

## Run examples

```powershell
.\runtime\scripts\run-mini-swe-preinstalled.ps1 `
  -TaskPath "tasks\batchline-submitted-by"

.\runtime\scripts\run-opencode-preinstalled.ps1 `
  -TaskPath "tasks\batchline-submitted-by"
```

Use `-KeepResolvedTask` only when inspecting/debugging the generated temporary binding.
