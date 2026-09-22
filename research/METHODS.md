# Research methods

## Unit of observation

A research observation is one recorded agent execution under a declared task version, harness profile, model/provider configuration, environment, timeout policy, and verifier revision. The final workspace establishes correctness; the trajectory supplies route evidence.

## Execution environment

The recorded experiments use Harbor 0.22.0 with Docker-backed task environments. Public harness cells use OpenCode 1.18.30 or Mini-SWE-Agent 2.4.6. The model is GLM-5.3-Flash served through Fireworks AI; Scenario 1 uses matched effective `max` reasoning across the recorded harness cells. The custom harness is treated as a private execution configuration and is not redistributed.

Exact task, harness, model, verifier, timeout, and run telemetry are retained with the recorded evidence. External software and service references are listed in `docs/provenance/software_attribution.md`.

## Evidence layers

The study keeps four layers distinct:

1. Task verifier: contract correctness.
2. Workspace observation: final-state scope and coarse diff statistics.
3. Run telemetry: calls, tokens, cache use, cost when available, and timing.
4. Trajectory: the sequence of observable interactions used for route analysis.

The first three layers remain in the shared task/evidence tree. Research interpretation is stored separately under `research/`.

## Route coding

The active coding vocabulary distinguishes inspection and transformation mechanism from artifact type. Examples include native full/range/continuation reads, shell text inspection, search/localization, structured parse/query, native string edit, whole-file write, shell/text-range mutation, and structured parse-transform-serialize. A read is coded as capped or continued only when truncation or explicit continuation is actually observed.

Recovery is classified by cause rather than by the fact that extra work occurred: implementation recovery, edit-route correction, verification-probe recovery, and environment/tool recovery are separate categories. Context stewardship includes anticipatory probing, re-grounding after edits, failure localization, requirement retention, repeated rediscovery, temporary verification artifacts, and work performed after the repository first reaches a green state.

The task-local Scenario 1 `EVALUATION_GUIDE.md` contains the operational coding procedure used for that scenario. Approved authoring and validation sources are indexed in `TASK_DESIGN_SOURCES.md`.

## Sampling interpretation

Two repetitions per Scenario 1 harness are treated as repeated case observations. They can demonstrate that a route or failure mode occurred, and can expose within-cell route variation, but they are not used as stable pass-rate estimates. Claims about recurrence are stated narrowly and tied to the observed trajectories.

Additional repetitions would be justified if the research objective shifts toward outcome distributions or reliability estimation. For the current route-oriented study, evidence across distinct calibrated task pressures can be more informative than repeatedly estimating success probability on one scenario.

## Custom-harness boundary

The custom harness participates as a black-box execution configuration in the published result surface. Its evidence includes correctness, verifier groups, timing, token/call telemetry, and workspace statistics. Its implementation and raw trajectories remain private, so no public route-level claim is based on those private artifacts.
