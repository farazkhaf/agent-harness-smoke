# Reference results

This file is the neutral product-facing result index. Interpretive route findings are kept under `research/`.

## Focused checkpoint

The v0.2.0 focused checkpoint contains 18 recorded runs: six tasks across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1. All 18 received `reward = 1.0` under their recorded task versions. Machine-readable forms are under `results/batchline-focused/accepted-18/`; the earlier 15-row checkpoint remains under `accepted-15/`.

## Scenario 1

Scenario 1 contains two recorded executions per harness under the same solver-visible task version `0.2.0`. The current verifier revision is r3. No recorded outcome differs between r2 and r3; r2 remains the revision that changed Custom Attempt 1 from the original r1 G5-only failure to pass after the contract audit.

| Harness | Attempt | Current outcome | Historical note |
|---|---:|---|---|
| OpenCode 1.18.30 | 1 | pass | passed r1 |
| OpenCode 1.18.30 | 2 | pass | passed r1 |
| Mini-SWE-Agent 2.4.6 | 1 | G1 fail | valid 600 s agent timeout; G1 defect unchanged by verifier revisions |
| Mini-SWE-Agent 2.4.6 | 2 | pass | passed r1 |
| custom-harness | 1 | pass | r1: G5 fail; r2+: pass after verifier-only contract correction |
| custom-harness | 2 | pass | passed r1 |

Canonical normalized Scenario 1 tables remain under `results/batchline-scenarios/batchline-scenario1-v0.2.0-comparison/`. Verifier r1/r2 history and the r3 evaluator are under `evidence/verifier-revisions/scenario1-v0.2.0/`.

These rows are reference outcomes, not product rankings or stable success-rate estimates. Calls, tokens, timing, workspace statistics, and verifier groups are retained as descriptive run telemetry.
