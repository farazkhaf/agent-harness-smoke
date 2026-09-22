# Scenario 1 results

Task version `0.2.0`; current verifier `r3`.

Output is non-reasoning completion output. Reasoning tokens are reported separately when available; provider-reported cost is retained independently.

| Harness | Attempt | Reward | Verifier groups | Calls | Input | Cached | Output | Reasoning | Cost USD | Total s |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `custom-harness` | 1 | 1.00 | G1 lifecycle:pass; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 25 | 1279891 | 1187840 | 12697 | 20324 | 0.0648 | 432.45 |
| `custom-harness` | 2 | 1.00 | G1 lifecycle:pass; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 32 | 1611711 | 1511424 | 16567 | 19495 | 0.0769 | 409.25 |
| `mini-swe-agent` | 1 | 0.00 | G1 lifecycle:fail; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 47 | 1181715 | 1077248 | 60210 | 46452 | 0.0781 | 671.19 |
| `mini-swe-agent` | 2 | 1.00 | G1 lifecycle:pass; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 43 | 1389312 | 1296384 | 44405 | 27136 | 0.0750 | 491.05 |
| `opencode` | 1 | 1.00 | G1 lifecycle:pass; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 45 | 1804749 | 1693696 | 12906 | 11918 | 0.0799 | 470.02 |
| `opencode` | 2 | 1.00 | G1 lifecycle:pass; G2 capacity health:pass; G3 public surfaces:pass; G4 event structure:pass; G5 event contract:pass; G6 integration preservation:pass | 42 | 1602556 | 1507328 | 11928 | 11633 | 0.0713 | 374.84 |

Run receipts and published trajectories are indexed under `evidence/public/scenario1/`. The original collection-time verifier is retained under `evidence/verifier-revisions/scenario1-v0.2.0/`.
