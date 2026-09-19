# Provenance

## Project identity

The project title is Agent Harness Smoke and the Harbor task namespace is `agent-harness-smoke`.

Version 0.1.0 publishes these task identities:

```text
agent-harness-smoke/batchline-submitted-by
agent-harness-smoke/batchline-selective-retry-policies
agent-harness-smoke/batchline-remove-legacy-remote-provider
agent-harness-smoke/batchline-quarantine-rate-limit-events
agent-harness-smoke/batchline-extract-legacy-remote-provider
```

The canonical runs were completed before the public namespace was finalized. Published run receipts map each archived run to its release task ID and retain hashes of the source execution artifacts. The task contracts and locked task versions are unchanged by the namespace change.

## Custom harness identity

The third harness is identified in release results as `custom-harness`, version `snapshot-1`. The result matrix contains its normalized correctness and resource fields; implementation and trajectory data are not distributed.

## Canonical runs

The accepted matrix contains one canonical run for each task/harness pair, for 15 rows in total.

## Task versions

| Family | Version |
|---|---:|
| B1 | 0.1.0 |
| R1 | 0.1.0 |
| R2 | 0.1.1 |
| R3 | 0.1.1 |
| R4 | 0.1.0 |

R2 and R3 use their corrected verifier versions consistently across all three harness rows.

## Authorship and release continuity

Agent Harness Smoke v0.1.0 is authored by Faraz Ul Khaf. `CITATION.cff`, `VERSION`, and `CHANGELOG.md` record the release identity and provide continuity for later task sets, repository fixtures, and scenario layers.
