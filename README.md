# Agent Harness Smoke

Agent Harness Smoke is a Harbor-native diagnostic suite for studying and validating how coding-agent harnesses interact with software workspaces under controlled task and model conditions. It is designed around **tightly specified software targets with unconstrained execution routes** rather than a global agent or harness leaderboard.

Version 0.2.0 contains six deterministic focused tasks plus Scenario 1 (`batchline-worker-draining-event-extraction`). The reusable product layer, retained execution evidence, and interpretive research layer are kept distinct inside the same repository.

## Repository layers

- `tasks/`, `runtime/`, `suites/` — reusable software/evaluation layer.
- `results/` — normalized reference results and verifier-group outcomes.
- `evidence/` — retained execution evidence, verifier history, and provenance.
- `docs/` — product-facing evaluation, reproducibility, and provenance documentation.
- `research/` — study objective, research methods, and interpretive findings.

The evidence layer is intentionally shared: prior trajectories and verifier records can help validate or understand a task without requiring users to reproduce the same expensive run, while research claims remain isolated under `research/`.

## Focused suite

| Family | Task ID | Interaction pressure | Task version |
|---|---|---|---|
| B1 | `agent-harness-smoke/batchline-submitted-by` | coordinated multi-file modification | 0.1.0 |
| R1 | `agent-harness-smoke/batchline-selective-retry-policies` | selective repeated editing | 0.1.0 |
| R2 | `agent-harness-smoke/batchline-remove-legacy-remote-provider` | substantial contiguous deletion | 0.1.1 |
| R3 | `agent-harness-smoke/batchline-quarantine-rate-limit-events` | large line-oriented inspection/filtering | 0.1.1 |
| R4 | `agent-harness-smoke/batchline-extract-legacy-remote-provider` | substantial move/module split | 0.1.0 |
| V1 | `agent-harness-smoke/batchline-shared-event-sequence-regression` | same-process behavioral verification | 0.1.0 |

The focused `accepted-18` checkpoint contains six tasks across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and a custom harness snapshot. All 18 recorded focused runs satisfy their task contracts. Historical focused reasoning configuration differs for the custom harness and is disclosed in provenance.

## Scenario 1

Scenario 1 is a separate composed maintenance task at solver-visible task version `0.2.0`. It has two recorded runs each for OpenCode, Mini-SWE-Agent, and the custom harness. Verifier revisions are versioned independently from the solver-visible task. Revision 1 is the collection-time evaluator; revision 2 corrected an overconstrained forwarding-alias interpretation; revision 3 adds contract-visible edge guards without changing any recorded Scenario 1 outcome.

See [`RESULTS.md`](RESULTS.md) for reference outcomes, [`docs/evaluation/scenario1_verifier_revision.md`](docs/evaluation/scenario1_verifier_revision.md) for verifier history, and [`research/scenario-1/FINDINGS.md`](research/scenario-1/FINDINGS.md) for interpretation.

## Documentation

- [`docs/evaluation/methodology.md`](docs/evaluation/methodology.md) — product/evaluation model.
- [`docs/evaluation/task_design.md`](docs/evaluation/task_design.md) — task and verifier design boundaries.
- [`docs/evaluation/scenario1_run_protocol.md`](docs/evaluation/scenario1_run_protocol.md) — Scenario 1 execution protocol.
- [`docs/reproducibility/`](docs/reproducibility/) — build, run, evidence, and privacy guidance.
- [`evidence/README.md`](evidence/README.md) — retained evidence layout.
- [`research/STUDY_OBJECTIVE.md`](research/STUDY_OBJECTIVE.md) — formal research objective.

## Citation

Agent Harness Smoke v0.2.0 is archived on Zenodo under DOI [`10.5281/zenodo.22895191`](https://doi.org/10.5281/zenodo.22895191). Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

## Quick run

From a Harbor-enabled PowerShell environment:

```powershell
.\runtime\scripts\build-mini-swe-runtime.ps1
.\runtime\scripts\build-opencode-runtime.ps1
.\runtime\scripts\run-focused-suite.ps1 -TrialsRoot "$PWD\trials"
```

Scenario 1 uses `runtime/scripts/run-scenario1.ps1`. Raw Harbor trials are written outside the release evidence tree; normalized results can be collected into `results/`.
