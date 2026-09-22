# Scenario 1 suite

This suite records two runs per included profile for `batchline-worker-draining-event-extraction` version `0.2.0`.

The bundled OpenCode and Mini-SWE profiles use GLM-5.3-Flash and omit `reasoning_effort`; the model therefore uses its documented default. No per-profile token, step, or cost cap is added. The task-level agent timeout is 600 seconds.

Run all included profiles:

```powershell
.\runtime\scripts\run-scenario1.ps1
```

Run one profile:

```powershell
.\runtime\scripts\run-scenario1.ps1 -ProfileId opencode-1.18.30
.\runtime\scripts\run-scenario1.ps1 -ProfileId mini-swe-2.4.6
```

Additional preinstalled or external profiles can be added using the same suite schema; see `docs/reproducibility/adding_harnesses.md`.
