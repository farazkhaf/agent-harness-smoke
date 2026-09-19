# Validation — agent-harness-smoke/batchline-extract-legacy-remote-provider 0.1.0

## Controls

| Control | Expected result |
|---|---|
| untouched starting state | fail / reward 0 |
| author extraction | pass / reward 1 |
| copy implementation to new module but leave original class | fail |
| remove class without creating destination module | fail |
| drop `legacy_remote` registration | fail |
| alternate valid implementation with locally factored inherited helper | pass |
| current-provider and representative legacy-provider behavior after author solution | pass |
| full repository tests and `make check` after author solution | pass |
| generic binder resolution for Mini-SWE 2.4.6 and OpenCode 1.18.30 | pass |

The starting `providers.py` is 572 lines (about 22 KB); the legacy provider occupies roughly 241 contiguous lines.

## Formal Harbor validation

The canonical task passes with `reward = 1.0` under OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
