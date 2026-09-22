# Scenario 1 run protocol

## Configuration

Scenario 1 uses `agent-harness-smoke/batchline-worker-draining-event-extraction` version `0.2.0`. The active suite definition is `suites/batchline-scenario1/suite.toml`.

The retained set contains two independent runs for each of these configurations:

- OpenCode 1.18.30;
- Mini-SWE-Agent 2.4.6;
- `custom-harness`.

All three use GLM-5.3-Flash at effective `max` reasoning. OpenCode and Mini-SWE omit `reasoning_effort`, which the model documents as defaulting to `max`; the custom configuration passes `max` explicitly. Each run uses the task-defined 600-second agent timeout and 180-second verifier timeout. No additional token, step, or cost cap is applied.

Runs for one harness may be collected separately from the others. Task version, harness version/profile, model configuration, timeout policy, and repeat count must remain fixed within a cell.

## Run validity

A run is valid when the declared task, harness, model, and environment execute and produce an interpretable Harbor trial, whether or not the verifier passes. Agent mistakes, verifier failure caused by the submitted workspace, and exhaustion of the declared agent timeout are recorded outcomes.

A run is invalid only when an exogenous problem prevents the intended execution or evaluation, for example an incorrect image/model, credential or provider failure before meaningful agent execution, environment startup failure, operator interruption, corrupted trial artifacts, or verifier infrastructure failure unrelated to the submitted workspace. Invalid trials should be retained with the reason recorded; a replacement uses the same declared configuration.

## Retained evidence

For each run retain the run/trial identifier and task identity, normalized report, verifier output, workspace observation, and trajectory when that trajectory is part of the published evidence surface. Raw Harbor stores may be retained privately without being included in a release.

Calls, tokens, cost, elapsed time, and workspace footprint are descriptive telemetry. Route claims must be traceable to retained observable evidence. The custom harness is published as a black-box configuration in the current evidence package, so public claims about its execution route are limited accordingly.

Correctness reports should identify the verifier revision used. Scenario 1 currently uses verifier `r3`; the collection-time verifier is retained separately for provenance.

## Additional harnesses

Additional harnesses can be added as new cells without modifying the task package. Before collecting a new cell, record the harness version, model/provider configuration, reasoning configuration when controlled, runtime image or external agent identity, timeout policy, and any harness-specific settings. See `docs/reproducibility/adding_harnesses.md` for the supported integration modes.
