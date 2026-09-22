# Scenario 1 run protocol

## Comparison definition

Scenario 1 uses `agent-harness-smoke/batchline-worker-draining-event-extraction` version `0.2.0`. The active suite definition is `suites/batchline-scenario1-comparison/suite.toml`.

The recorded comparison contains two independent runs for each of these harness profiles:

- OpenCode 1.18.30
- Mini-SWE-Agent 2.4.6
- custom harness `coding-agent-pyworkspace` 0.2.0.dev0-harbor.2 (reported publicly as `custom-harness`)

All profiles use GLM-5.3-Flash at the model's `max` reasoning setting. OpenCode and Mini-SWE omit `reasoning_effort`, which GLM-5.3-Flash documents as defaulting to `max`; the custom Scenario 1 profile passes `max` explicitly. The OpenCode and Mini-SWE provider identifiers use the spelling expected by their respective integrations.

Each run uses the task-defined 600-second agent timeout and 180-second verifier timeout. No additional per-harness token, step, or cost cap is applied.

The two runs for a harness may be collected separately from other harness cells. The task version, harness profile, model, timeout settings, and repeat count must remain unchanged within a cell.

## Run validity

A run is valid when the declared task, harness, model, and environment execute and produce an interpretable Harbor trial, regardless of whether the verifier passes. Agent errors, verifier failure due to the submitted workspace, or exhaustion of the declared 600-second agent timeout are outcomes rather than grounds for replacement.

A run may be marked invalid only for an exogenous execution problem such as an incorrect image or model, credential or service failure before meaningful agent execution, environment startup failure, operator interruption, corrupted/missing trial artifacts, or verifier infrastructure failure unrelated to the submitted workspace. Invalid trials should be retained with the reason recorded; a replacement uses the same declared configuration.

## Retained evidence

For each run retain:

- Harbor `result.json` and task/runtime metadata;
- normalized report;
- verifier group artifact;
- workspace observer artifact;
- ATIF/native trajectory sufficient to support route analysis;
- run/trial identifier and task checksum.

Compact reports summarize outcomes and resource telemetry. Route claims should be traceable to the retained trajectory or workspace evidence. Calls, tokens, cost, and elapsed time are descriptive and are not combined into a harness score. The custom harness may remain black-box at the public evidence layer; in that case public claims about it are limited to the exposed outcome/telemetry surface unless a sanitized route trace is later released.

Correctness records also carry a verifier revision independently of task version. Verifier revision 1 is historical; revision 2 records the contract correction that changed Custom Attempt 1; revision 3 is the current evaluator and adds only contract-visible edge guards that do not change any recorded outcome. Verifier-only maintenance does not require repeating agent executions when solver-visible inputs are unchanged.

## Extension harnesses

Additional harnesses may be appended later as new comparison cells. Before collecting the first run for an added harness, record its harness version, model/provider configuration, reasoning configuration if explicitly controlled, runtime image or implementation identifier, and any harness-specific settings. Added cells use two independent runs unless a later protocol version states otherwise.
