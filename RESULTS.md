# Recorded results

This index summarizes the reference executions included with the release. Machine-readable tables are under `results/`, execution artifacts are under `evidence/`, and interpretation is kept separately under `research/`.

## Focused suite

The focused checkpoint carried by v0.2.1 contains 18 recorded runs: six tasks across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1. All 18 received `reward = 1.0` under their recorded task versions.

Results: `results/batchline-focused/accepted-18/`.

## Scenario 1

Scenario 1 contains two recorded executions per harness under task version `0.2.0`. The table below uses the current verifier, revision `r3`.

| Harness | Attempt | Outcome | Note |
|---|---:|---|---|
| OpenCode 1.18.30 | 1 | pass | — |
| OpenCode 1.18.30 | 2 | pass | — |
| Mini-SWE-Agent 2.4.6 | 1 | G1 fail | valid 600 s agent timeout; the final workspace retained a lifecycle invariant defect |
| Mini-SWE-Agent 2.4.6 | 2 | pass | — |
| custom-harness | 1 | pass | the original collection-time verifier rejected its forwarding-alias schema layout; the current verifier accepts the unchanged workspace because concrete worker definitions reside in the dedicated worker schema |
| custom-harness | 2 | pass | — |

Current normalized results: `results/batchline-scenarios/scenario1/`.

The original collection-time verifier and the direct original-to-current verifier diff are preserved under `evidence/verifier-revisions/scenario1-v0.2.0/`. OpenCode and Mini-SWE Scenario 1 trajectories are published under `evidence/public/scenario1/`; custom-harness run receipts and verifier records are included there, while its raw trajectory remains private.

Two attempts per harness are retained as repeated observations. Their sampling interpretation and route analysis are documented under `research/`.
