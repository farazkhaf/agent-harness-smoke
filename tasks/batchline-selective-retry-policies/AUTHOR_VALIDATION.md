# Validation — agent-harness-smoke/batchline-selective-retry-policies 0.1.0

## Controls

| Control | Expected result |
|---|---|
| untouched starting state | fail / reward 0 |
| author solution | pass / reward 1 |
| replace every `standard` retry policy | fail |
| update only one target | fail |
| policy validation after author solution | pass |
| full Batchline `make check` after author solution | pass (55 tests) |
| generic binder resolution for Mini-SWE 2.4.6 and OpenCode 1.18.30 | pass |

The policy catalog contains 20 job tables across 542 lines, with the three targets separated across the file.

## Formal Harbor validation

The canonical task passes with `reward = 1.0` under OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
