# Batchline focused-task suite

This suite defines the six focused tasks in Agent Harness Smoke v0.2.0.

| Family | Task | Primary interaction |
|---|---|---|
| B1 | `agent-harness-smoke/batchline-submitted-by` | coordinated multi-file modification |
| R1 | `agent-harness-smoke/batchline-selective-retry-policies` | selective repeated edit |
| R2 | `agent-harness-smoke/batchline-remove-legacy-remote-provider` | large contiguous deletion |
| R3 | `agent-harness-smoke/batchline-quarantine-rate-limit-events` | large line-oriented inspection/filtering |
| R4 | `agent-harness-smoke/batchline-extract-legacy-remote-provider` | large contiguous move/module split |
| V1 | `agent-harness-smoke/batchline-shared-event-sequence-regression` | same-process behavioral verification with constrained regression artifact |

The runnable public suite uses OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6 with the same GLM-5.3-Flash model through their harness-native Fireworks provider identifiers. The canonical result matrix additionally contains one normalized `custom-harness` snapshot-1 row per task.

## Run

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TrialsRoot "$PWD\trials"
```

Preview without launching trials:

```powershell
.\runtime\scripts\run-focused-suite.ps1 -PlanOnly
```

Selected cells can be run with `-TaskId` and `-ProfileId`; focused tasks are independent and adding V1 does not imply rerunning earlier task cells. The runnable public matrix now contains 12 cells: six tasks by two public harness profiles. The accepted 18-row checkpoint adds six normalized custom-harness rows.

Resource fields describe individual routes and are not combined into an efficiency score.
