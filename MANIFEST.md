# Release manifest

Agent Harness Smoke v0.2.0 contains:

- six focused Harbor task packages and Scenario 1 under `tasks/`;
- version-pinned OpenCode and Mini-SWE runtime wrappers/profiles plus generic binding/reporting utilities;
- focused and Scenario 1 suite definitions;
- normalized reference results under `results/`;
- public run evidence and Scenario 1 verifier history under `evidence/`;
- product-facing evaluation/reproducibility documentation under `docs/`;
- a separate interpretive research layer under `research/`;
- release metadata in `VERSION`, `CHANGELOG.md`, `CITATION.cff`, and `LICENSE`.

The custom harness is represented at the public evidence layer through black-box outcomes and neutral telemetry. Its implementation, prompts, tool schemas, and raw private trajectory are not included.

Two release artifacts can be produced from this tree: a core package that excludes `research/`, and a study snapshot that includes the full research layer. Both share the same tasks, results, and evidence.
