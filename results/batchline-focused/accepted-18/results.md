# Focused-suite results

Recorded v0.2.0 checkpoint for B1, R1-R4, and V1. Calls, tokens, cost, and elapsed time are descriptive run telemetry; retained trajectories and verifier artifacts are stored separately under `evidence/`.

Output is non-reasoning completion output. Reasoning tokens are reported separately when available; provider-reported cost is retained independently.

## Runs

| Task | Harness | Reward | Verifier groups | Calls | Input | Cached | Output | Reasoning | Cost USD | Total s |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `custom-harness` | 1.00 | — | 22 | 417196 | 346112 | 3049 | 1340 | 0.0229 | 182.04 |
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `mini-swe-agent` | 1.00 | — | 22 | 334192 | 288768 | 7233 | 2993 | 0.0191 | 268.42 |
| `agent-harness-smoke/batchline-extract-legacy-remote-provider` | `opencode` | 1.00 | — | 13 | 207203 | 176128 | 2861 | 556 | 0.0117 | 219.58 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `custom-harness` | 1.00 | — | 4 | 26219 | 16384 | 739 | 23 | 0.0023 | 130.52 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `mini-swe-agent` | 1.00 | — | 16 | 84284 | 51200 | 3092 | 593 | 0.0080 | 132.03 |
| `agent-harness-smoke/batchline-quarantine-rate-limit-events` | `opencode` | 1.00 | — | 4 | 30906 | 18432 | 300 | 59 | 0.0026 | 106.39 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `custom-harness` | 1.00 | — | 12 | 189023 | 157696 | 1423 | 336 | 0.0102 | 99.88 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `mini-swe-agent` | 1.00 | — | 31 | 337441 | 276480 | 4224 | 969 | 0.0196 | 180.19 |
| `agent-harness-smoke/batchline-remove-legacy-remote-provider` | `opencode` | 1.00 | — | 16 | 296787 | 258048 | 1218 | 3571 | 0.0159 | 272.05 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `custom-harness` | 1.00 | — | 7 | 80936 | 59392 | 878 | 305 | 0.0055 | 130.29 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `mini-swe-agent` | 1.00 | — | 12 | 63336 | 36864 | 962 | 132 | 0.0056 | 252.19 |
| `agent-harness-smoke/batchline-selective-retry-policies` | `opencode` | 1.00 | — | 14 | 139027 | 116736 | 1205 | 314 | 0.0076 | 184.99 |
| `agent-harness-smoke/batchline-shared-event-sequence-regression` | `custom-harness` | 1.00 | — | 12 | 134510 | 110592 | 1578 | 346 | 0.0078 | 165.95 |
| `agent-harness-smoke/batchline-shared-event-sequence-regression` | `mini-swe-agent` | 1.00 | — | 15 | 121555 | 96256 | 4139 | 764 | 0.0088 | 241.19 |
| `agent-harness-smoke/batchline-shared-event-sequence-regression` | `opencode` | 1.00 | — | 14 | 191747 | 161792 | 1186 | 1262 | 0.0106 | 230.77 |
| `agent-harness-smoke/batchline-submitted-by` | `custom-harness` | 1.00 | — | 6 | 61661 | 43008 | 1344 | 251 | 0.0048 | 139.43 |
| `agent-harness-smoke/batchline-submitted-by` | `mini-swe-agent` | 1.00 | — | 20 | 143568 | 112640 | 3356 | 1034 | 0.0097 | 190.91 |
| `agent-harness-smoke/batchline-submitted-by` | `opencode` | 1.00 | — | 11 | 121055 | 100352 | 1398 | 448 | 0.0070 | 185.93 |
