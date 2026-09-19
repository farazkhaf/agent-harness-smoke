# Validation — agent-harness-smoke/batchline-remove-legacy-remote-provider 0.1.1

## Controls

| Control | Expected result |
|---|---|
| untouched starting state | fail / reward 0 |
| author solution | pass / reward 1 |
| remove registry entry but leave the class | fail |
| remove implementation but leave stale positive compatibility coverage | fail |
| add negative rejection coverage mentioning `legacy_remote` | allowed |
| current-provider behavior after author solution | pass |
| full repository tests and `make check` after author solution | pass |
| generic binder resolution for Mini-SWE 2.4.6 and OpenCode 1.18.30 | pass |

The starting `providers.py` contains a legacy implementation of roughly 239 contiguous lines.

## Formal Harbor validation

Version 0.1.1 passes with `reward = 1.0` under OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
