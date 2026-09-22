# Scenario 1 comparison suite

This suite defines the public Scenario 1 comparison for task version `0.2.0`. It contains two independent runs per included harness profile.

The included profiles use GLM-5.3-Flash and do not pass an explicit `reasoning_effort`. GLM-5.3-Flash uses `max` when the parameter is omitted. No additional per-harness token, step, or cost budget is imposed. The task-level agent timeout is 600 seconds for every harness.

Run both included harnesses:

```powershell
.\runtime\scripts\run-scenario1.ps1
```

Run one harness cell at a time:

```powershell
.\runtime\scripts\run-scenario1.ps1 -ProfileId opencode-1.18.30
.\runtime\scripts\run-scenario1.ps1 -ProfileId mini-swe-2.4.6
```

When `-OutputRoot` is omitted, the generic runner places scenario results under `results\batchline-scenarios\<suite-id>\<timestamp>`. Raw Harbor trials remain under `trials/`.
