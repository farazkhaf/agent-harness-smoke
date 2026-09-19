# Validation — agent-harness-smoke/batchline-submitted-by 0.1.0

## Controls

| Control | Expected result |
|---|---|
| untouched starting state | fail / reward 0 |
| author solution | pass / reward 1 |
| existing Batchline public tests after author solution | 48 passed |
| production configuration validation after author solution | pass |
| bundled event validation after author solution | pass |

Deliberately incomplete implementations were confirmed to fail when they omitted service propagation, `Job.from_mapping()` propagation, full/summary API serialization, or CLI detail rendering.

The author solution is one valid implementation rather than a required patch shape.

## Formal Harbor validation

The canonical task passes with `reward = 1.0` under OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1.
