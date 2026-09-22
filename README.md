# Agent Harness Smoke

Agent Harness Smoke is a Harbor-native diagnostic suite for exercising coding-agent workspace interaction under controlled software tasks. Each task defines a reproducible starting repository and an explicit software contract while leaving the execution route unconstrained.

Version 0.2.1 includes six focused tasks, one composed scenario, reusable runtime binding for preinstalled and external Harbor agents, normalized reporting, retained reference evidence, and an active research layer.

## Repository layout

- `tasks/` contains the Harbor task packages and task-specific design and validation records.
- `runtime/` contains reusable agent integration, task binding, reporting, and suite utilities.
- `suites/` contains the focused suite and Scenario 1 suite definitions.
- `results/` contains recorded result summaries.
- `evidence/` contains published trajectories, receipts, verifier output, and evaluator provenance.
- `docs/` contains usage, evaluation, reproducibility, and software provenance documentation.
- `research/` contains the study objective, methods, task-design source index, and findings.

## Focused tasks

| Family | Task | Interaction pressure | Version |
|---|---|---|---|
| B1 | `batchline-submitted-by` | coordinated multi-file modification | 0.1.0 |
| R1 | `batchline-selective-retry-policies` | selective repeated editing | 0.1.0 |
| R2 | `batchline-remove-legacy-remote-provider` | substantial contiguous deletion | 0.1.1 |
| R3 | `batchline-quarantine-rate-limit-events` | large line-oriented inspection/filtering | 0.1.1 |
| R4 | `batchline-extract-legacy-remote-provider` | substantial move/module split | 0.1.0 |
| V1 | `batchline-shared-event-sequence-regression` | same-process behavioral verification | 0.1.0 |

The recorded focused checkpoint contains 18 accepted executions across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1. See [`RESULTS.md`](RESULTS.md).

## Scenario 1

`batchline-worker-draining-event-extraction` composes coordinated lifecycle work with Python extraction, JSON-Schema extraction, and constrained verification. Two recorded executions are retained for each of the three harness configurations. Recorded Scenario 1 results use verifier revision `r3`; the collection-time evaluator is retained separately because one recorded workspace required verifier adjudication without an agent rerun.

See [`results/batchline-scenarios/scenario1/`](results/batchline-scenarios/scenario1/) and [`docs/provenance/scenario1_verifier_history.md`](docs/provenance/scenario1_verifier_history.md).

## Research layer

The study asks how coding-agent harnesses mediate realized software-engineering interaction routes: which workspace primitives are selected, how inspection and transformation are composed, where requirement retention and recovery appear, and how harness affordances are used or substituted. Correctness anchors each trajectory against a common task contract; the current evidence supports descriptive route and failure analysis rather than stable harness-wide reliability, speed, or cost rankings.

See [`research/STUDY_OBJECTIVE.md`](research/STUDY_OBJECTIVE.md), [`research/METHODS.md`](research/METHODS.md), [`research/TASK_DESIGN_SOURCES.md`](research/TASK_DESIGN_SOURCES.md), and [`research/scenario-1/FINDINGS.md`](research/scenario-1/FINDINGS.md).

## Harness integration

The included OpenCode and Mini-SWE profiles are reference integrations, not a closed set. The suite runner supports two extension paths:

- `preinstalled`: bind an agent-agnostic task to a reusable, version-pinned runtime image through a runtime profile;
- `external`: run any Harbor agent import path that is already available to the host Harbor process, with model configuration either supplied by the suite or owned by the agent.

This allows a new agent to be integrated once and reused across the task suite without maintaining agent-specific copies of tasks. See [`docs/reproducibility/adding_harnesses.md`](docs/reproducibility/adding_harnesses.md) and [`runtime/BINDING.md`](runtime/BINDING.md).

## Release and citation

The Git tag identifies the canonical source tree for a release, and the corresponding Zenodo archive provides persistent citation. Recorded executions use Harbor 0.22.0 with Docker-backed task environments. The public harness configurations use OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6; recorded model inference uses GLM-5.3-Flash served through Fireworks AI.

See [`docs/provenance/software_attribution.md`](docs/provenance/software_attribution.md) for software references and [`CITATION.cff`](CITATION.cff) for citation metadata. Agent Harness Smoke v0.2.1 is archived on Zenodo under DOI [`10.5281/zenodo.22897087`](https://doi.org/10.5281/zenodo.22897087).

## Quick start

From a Harbor-enabled PowerShell environment:

```powershell
.\runtime\scripts\build-mini-swe-runtime.ps1
.\runtime\scripts\build-opencode-runtime.ps1
.\runtime\scripts\run-focused-suite.ps1 -TrialsRoot "$PWD\trials"
```

Scenario 1 uses `runtime/scripts/run-scenario1.ps1`. Raw Harbor trials are stored separately from the curated evidence included in the release.
