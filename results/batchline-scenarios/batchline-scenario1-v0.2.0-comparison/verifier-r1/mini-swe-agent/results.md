# batchline-scenario1-v0.2.0-comparison results

Scenario 1 comparison: worker drain/resume lifecycle with Python and JSON Schema extraction

> Compact suite report only. Raw Harbor/native trajectories remain separate drill-down artifacts and are not interpreted here. Calls/tokens/cost/time are descriptive route/resource telemetry; smaller wall time is not treated as inherently better.

## Runs

| Task | Harness | Attempt | Reward | Verifier groups | Calls | Input | Cached | Output | Cost USD | Total s |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `mini-swe-agent` | 1 | 0.00 | G1_lifecycle=fail, G2_capacity_health=pass, G3_public_surfaces=pass, G4_event_structure=pass, G5_event_contract=pass, G6_integration_preservation=pass | 47 | 1181715 | 1077248 | 60210 | 0.0781 | 671.19 |
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `mini-swe-agent` | 2 | 1.00 | G1_lifecycle=pass, G2_capacity_health=pass, G3_public_surfaces=pass, G4_event_structure=pass, G5_event_contract=pass, G6_integration_preservation=pass | 43 | 1389312 | 1296384 | 44405 | 0.0750 | 491.05 |

## Repeated-run aggregates

| Task | Harness | Runs | Pass rate | Median reward | Median calls | Median input | Median output | Median cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-worker-draining-event-extraction` | `mini-swe-agent` | 2 | 0.50 | 0.5000 | 45.00 | 1285513.50 | 52307.50 | 0.0766 |
