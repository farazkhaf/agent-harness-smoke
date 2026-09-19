# Agent Harness Smoke

Agent Harness Smoke is a Harbor-native evaluation suite for studying how coding-agent harnesses interact with software workspaces under controlled task and model conditions.

Version 0.1.0 uses Batchline, a small Python fixture repository, and defines five deterministic focused tasks. The canonical checkpoint contains 15 Harbor runs: five tasks across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and a custom harness snapshot. All 15 canonical runs satisfy their task contracts with `reward = 1.0`.

The suite is intended for conformance and interaction analysis rather than global agent ranking. Task verifiers determine correctness. Workspace observations describe the resulting repository state, while trajectories provide evidence about the route taken to reach it. Calls, tokens, cost, and elapsed time are reported as end-to-end run telemetry and are not combined into an efficiency score.

## Documentation

- [Results and findings](RESULTS.md) presents the canonical matrix, resource observations, workspace observations, and trajectory-supported findings.
- [Methodology](docs/methodology.md) describes the evaluation model and comparison rules.
- [Reproducibility](docs/reproducibility.md) covers runtime builds, execution, normalization, and collection.
- [Task design](docs/task_design.md) describes the focused-task families and verifier boundaries.
- [Evidence and privacy](docs/evidence_and_privacy.md) describes the published evidence set and custom-harness boundary.
- [Provenance](PROVENANCE.md) records public task identities, task versions, authorship, and canonical-run conventions.
- [Validation](VALIDATION.md) summarizes task, runtime, and formal matrix validation.

## Release overview

| Family | Task ID | Interaction primitive | Task version |
|---|---|---|---|
| B1 | `agent-harness-smoke/batchline-submitted-by` | coordinated multi-file modification | 0.1.0 |
| R1 | `agent-harness-smoke/batchline-selective-retry-policies` | selective repeated edit | 0.1.0 |
| R2 | `agent-harness-smoke/batchline-remove-legacy-remote-provider` | large contiguous deletion | 0.1.1 |
| R3 | `agent-harness-smoke/batchline-quarantine-rate-limit-events` | large line-oriented inspection/filtering | 0.1.1 |
| R4 | `agent-harness-smoke/batchline-extract-legacy-remote-provider` | large contiguous move/module split | 0.1.0 |

Machine-readable results are under [`results/batchline-focused/accepted-15/`](results/batchline-focused/accepted-15/). Public run evidence for OpenCode and Mini-SWE is under [`evidence/public/`](evidence/public/).

## Release metadata

Agent Harness Smoke v0.1.0 was released on 2026-09-19 by Faraz Ul Khaf under the [MIT License](LICENSE). Citation metadata is provided in [`CITATION.cff`](CITATION.cff), and release history is recorded in [`CHANGELOG.md`](CHANGELOG.md).

Suggested citation:

> Faraz Ul Khaf. *Agent Harness Smoke*, v0.1.0 (2026).

## Quick run

From a Harbor-enabled PowerShell environment, build the reusable public harness images:

```powershell
.\runtime\scripts\build-mini-swe-runtime.ps1
.\runtime\scripts\build-opencode-runtime.ps1
```

Run the focused suite:

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TrialsRoot "$PWD\trials"
```

Raw Harbor trials are written under `trials/`; normalized comparison output is written under `results/`. See the [reproducibility guide](docs/reproducibility.md) for the complete workflow.
