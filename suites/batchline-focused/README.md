# Batchline focused-task suite

This suite defines the five Batchline focused tasks in Agent Harness Smoke v0.1.0.

| Family | Task | Primary interaction |
|---|---|---|
| B1 | `agent-harness-smoke/batchline-submitted-by` | coordinated multi-file modification |
| R1 | `agent-harness-smoke/batchline-selective-retry-policies` | selective repeated edit |
| R2 | `agent-harness-smoke/batchline-remove-legacy-remote-provider` | large contiguous deletion |
| R3 | `agent-harness-smoke/batchline-quarantine-rate-limit-events` | large line-oriented inspection/filtering |
| R4 | `agent-harness-smoke/batchline-extract-legacy-remote-provider` | large contiguous move/module split |

The runnable public suite uses OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6 with the same GLM-5.3-Flash model through their harness-native Fireworks provider identifiers. The release result matrix also contains five normalized rows from `custom-harness` snapshot-1.

## Run

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TrialsRoot "$PWD\trials"
```

Preview without launching trials:

```powershell
.\runtime\scripts\run-focused-suite.ps1 -PlanOnly
```

Run a selected cell:

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TaskId "agent-harness-smoke/batchline-extract-legacy-remote-provider" `
  -ProfileId "mini-swe-2.4.6" `
  -TrialsRoot "$PWD\trials"
```

The runner normalizes completed trials and emits `results.json`, `results.csv`, and `results.md`. The runnable public matrix contains 10 cells: five tasks by two public harness profiles.

R2 and R3 are version 0.1.1; B1, R1, and R4 are version 0.1.0.

## Reporting

Compact reports contain task, harness, model, reward, model-call count, token/cache totals, cost, and timing when available. Trajectories are stored separately as route evidence. Resource fields describe individual runs and are not combined into an efficiency score.
