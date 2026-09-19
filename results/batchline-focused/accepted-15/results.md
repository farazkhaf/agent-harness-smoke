# batchline-focused-v0.1 results

Canonical Agent Harness Smoke focused-task checkpoint: B1 plus R1-R4.

This table is the compact canonical result matrix. OpenCode and Mini-SWE trajectories are stored separately under `evidence/public/`. Calls, token totals, cost, and timing describe individual run routes; they are not combined into an efficiency score.

## Runs

| Task | Harness | Reward | Calls | Input | Cached | Output | Cost USD | Total s |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `custom-harness` | 1.00 | 22 | 417196 | 346112 | 4389 | 0.0229 | 182.04 |
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `mini-swe-agent` | 1.00 | 22 | 334192 | 288768 | 7233 | 0.0191 | 268.42 |
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `opencode` | 1.00 | 13 | 207203 | 176128 | 2861 | 0.0117 | 219.58 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `custom-harness` | 1.00 | 4 | 26219 | 16384 | 762 | 0.0023 | 130.52 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `mini-swe-agent` | 1.00 | 16 | 84284 | 51200 | 3092 | 0.0080 | 132.03 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `opencode` | 1.00 | 4 | 30906 | 18432 | 300 | 0.0026 | 106.39 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `custom-harness` | 1.00 | 12 | 189023 | 157696 | 1759 | 0.0102 | 99.88 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `mini-swe-agent` | 1.00 | 31 | 337441 | 276480 | 4224 | 0.0196 | 180.19 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `opencode` | 1.00 | 16 | 296787 | 258048 | 1218 | 0.0159 | 272.05 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `custom-harness` | 1.00 | 7 | 80936 | 59392 | 1183 | 0.0055 | 130.29 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `mini-swe-agent` | 1.00 | 12 | 63336 | 36864 | 962 | 0.0056 | 252.19 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `opencode` | 1.00 | 14 | 139027 | 116736 | 1205 | 0.0076 | 184.99 |
| `agent-harness-smoke/batchline-submitted-by` | `custom-harness` | 1.00 | 6 | 61661 | 43008 | 1595 | 0.0048 | 139.43 |
| `agent-harness-smoke/batchline-submitted-by` | `mini-swe-agent` | 1.00 | 20 | 143568 | 112640 | 3356 | 0.0097 | 190.91 |
| `agent-harness-smoke/batchline-submitted-by` | `opencode` | 1.00 | 11 | 121055 | 100352 | 1398 | 0.0070 | 185.93 |
