# Validation — agent-harness-smoke/batchline-quarantine-rate-limit-events 0.1.1

## Controls

| Control | Expected result |
|---|---|
| untouched starting state | fail / reward 0 |
| author streaming solution | pass / reward 1 |
| correct IDs in reverse order | fail |
| modified incident archive with otherwise correct output | fail |
| full Batchline `make check` after author solution | pass (55 tests) |
| generic binder resolution for Mini-SWE 2.4.6 and OpenCode 1.18.30 | pass |

The generated archive contains 18,000 JSONL records (about 3.94 MB), of which ten match the task filter.

## Formal Harbor validation

Version 0.1.1 passes with `reward = 1.0` under OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
