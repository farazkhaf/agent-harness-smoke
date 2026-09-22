# batchline-scenario1-v0.2.0-comparison results

Scenario 1 comparison: worker drain/resume lifecycle with Python and JSON Schema extraction

> Compact suite report only. Raw Harbor/native trajectories remain separate drill-down artifacts and are not interpreted here. Calls/tokens/cost/time are descriptive route/resource telemetry; smaller wall time is not treated as inherently better.

## Runs

| Task | Harness | Attempt | Reward | Verifier groups | Calls | Input | Cached | Output | Cost USD | Total s |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `opencode` | 1 | 1.00 | G1_lifecycle=pass, G2_capacity_health=pass, G3_public_surfaces=pass, G4_event_structure=pass, G5_event_contract=pass, G6_integration_preservation=pass | 45 | 1804749 | 1693696 | 12906 | 0.0799 | 470.02 |
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `opencode` | 2 | 1.00 | G1_lifecycle=pass, G2_capacity_health=pass, G3_public_surfaces=pass, G4_event_structure=pass, G5_event_contract=pass, G6_integration_preservation=pass | 42 | 1602556 | 1507328 | 11928 | 0.0713 | 374.84 |

## Repeated-run aggregates

| Task | Harness | Runs | Pass rate | Median reward | Median calls | Median input | Median output | Median cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `opencode` | 2 | 1.00 | 1.00 | 43.50 | 1703652.50 | 12417.00 | 0.0756 |
