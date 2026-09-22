# Scenario 1 run evaluation guide

This guide defines the analysis procedure for repeated runs of `agent-harness-smoke/batchline-worker-draining-event-extraction` version `0.2.0`. Correctness is determined by the task verifier. Trajectory analysis is descriptive: it reconstructs how a run reached its final state and does not change the reward.

## Evidence model

Four evidence layers are used. They should be interpreted independently before they are combined in a run narrative.

| Evidence | Role |
|---|---|
| Verifier output | Establishes whether the submitted workspace satisfies the software contract. |
| Workspace observation | Records final changed paths and edit footprint. |
| Trajectory | Records observable inspection, editing, execution, validation, and recovery. |
| Telemetry | Records calls, token use, cost, and elapsed time for the observed execution. |

A final diff does not establish how a change was produced. Likewise, non-use of a tool or harness affordance does not establish that the affordance was unavailable.

## Unit of analysis and milestones

The primary unit is one complete run. Within a run, reconstruct operation episodes rather than treating every tool call as an independent event. When the trajectory supports them, record the end of initial repository orientation, the first workspace modification, major changes in edit route, the first successful core correctness check, the first successful complete repository validation, and the final workspace review.

A core correctness check may combine the repository test suite with task-specific validation such as event-example validation. Complete repository validation means the repository's declared validation workflow, normally `make check` or an equivalent set of native commands, has succeeded. Keeping these milestones separate helps distinguish implementation work from later verification and review overhead.

## Repository inspection and localization

Code the interaction primitive that is actually used, independently of file type.

| Code | Description |
|---|---|
| Native full read | A repository read operation returns the requested file as one view. |
| Native range read | A read is explicitly limited to a range or offset. |
| Continuation read | The agent continues from an earlier bounded or truncated read. |
| Shell text inspection | `cat`, `sed`, `head`, `tail`, or a comparable shell operation is used to inspect text. |
| Search/localization | `grep`, `rg`, globbing, or another search mechanism identifies relevant paths or regions. |
| Structured parse/query | A script or language runtime parses an artifact and inspects it structurally. |

Do not classify a read as capped merely because the file is large. Capped traversal requires observable truncation or an explicit continuation/range operation. For shell-oriented harnesses, also record when several logical files are concatenated into one observation and whether the harness elides the middle of long output. Observation truncation is an interface property; its research relevance comes from how the run compensates for or overlooks the missing context.

For `schemas/events.schema.json`, record whether the run reads the file directly, localizes selected definitions, parses it structurally, or combines those approaches. The analysis describes the route; it does not prescribe one.

## Transformation routes

The scenario contains three coupled transformation surfaces.

Worker lifecycle coordination spans the worker model, registry/capacity behavior, serializer, CLI rendering/actions, event registry, examples, and validation. The analysis should note how the run keeps those surfaces synchronized and whether previously established requirements are preserved as work moves between them.

Python event extraction moves worker constructor ownership to `worker_events.py` while preserving compatibility through `encoder.py` and maintaining one process-wide event-ID sequence. Record whether the extraction is performed incrementally, through a whole-file reconstruction, with script-assisted removal, or by another mechanism.

Worker-schema extraction moves worker definitions out of `events.schema.json`, rewires worker references, and preserves non-worker definitions. Useful transformation categories include local textual replacement, whole-file rewrite, line/range deletion, structured parse-transform-serialize, and combinations of these methods.

The task does not require an edit primitive to fail. A route change caused by operation shape is evidence even when every tool call succeeds.

## Recovery classification

Recovery episodes are classified by cause rather than counted as a single retry category.

| Class | Definition |
|---|---|
| Implementation defect | The edited repository contains incorrect product or integration behavior and execution reveals it. |
| Incomplete transformation | An edit succeeds mechanically but leaves required old content or misses part of the intended change. |
| Edit-route correction | The agent changes editing mechanism after recognizing that the current route is incomplete or awkward. |
| Verification-probe defect | A temporary solver-authored assertion, script, or check is wrong while the repository state is correct with respect to that assertion. |
| Command/tool invocation issue | The intended operation is sound but the invocation, syntax, or tool use is incorrect. |
| Environment/infrastructure issue | The problem is external to the submitted workspace and agent-authored logic. |

For each recovery episode, record where it begins, what evidence is used to localize the issue, whether product files change, and where the run returns to a validated state.

## Context stewardship

Context stewardship concerns how the run preserves and reuses task-relevant state across a long, multi-surface change; it is not a proxy for low token use. Relevant evidence includes useful pre-implementation probes, targeted rereads after meaningful workspace changes, repeated rediscovery without an intervening state change, localization behavior after a failure, and whether requirements established on one surface remain available while work proceeds on another. A particularly important case is requirement retention: if a run explicitly identifies an invariant during planning, record whether that invariant survives into the implementation and into any solver-authored verification.

Harness execution semantics are part of this analysis. Record whether command working directory or environment persists across calls, whether the model must restate state such as `cd` or `PYTHONPATH`, whether multiple artifacts are combined into one shell observation, and whether shell pipelines can obscure the exit status of an upstream command. These conditions are not treated as defects by themselves; they describe the interaction burden presented by the harness.

Temporary verification work also belongs here. Externalizing a long check into a temporary file can improve line-level diagnosis even though the file never appears in the submitted workspace. Conversely, a self-authored check that consumes several additional calls after substantial correctness evidence is already available is meaningful verification overhead and should be reported as such.

## Verification route

Record the sequence of repository-native tests, task-specific validation, independent probes, and optional counterfactual checks. The required final test-source scope is narrow: only the existing schema-location test may change. Temporary checks are valid execution routes but are not required for correctness and should be analyzed separately from repository modifications.

For shared process state, record the mechanism actually used to verify event-ID continuity. A reusable test, one-shot Python process, persistent interpreter, shell command, or another valid route may all provide evidence.

Also record the completion boundary. Distinguish the first green repository-native validation from later optional verification/review, and note whether the harness reaches its normal completion/submission action before the declared agent budget. A run that remains active until the declared agent timeout is a valid observed outcome unless independent evidence shows an infrastructure/provider failure prevented normal execution.

## Workspace footprint

Observer schema `0.2` separates tracked Git changes from untracked text additions.

| Field | Interpretation |
|---|---|
| `workspace_lines_added`, `workspace_lines_deleted` | Tracked `git diff --numstat` changes. |
| `workspace_untracked_text_lines_added` | UTF-8 text lines in untracked files returned by `git ls-files --others --exclude-standard`. |
| `workspace_text_lines_added_total` | Tracked additions plus untracked text additions. |
| `workspace_changed_files_total` | Tracked and untracked changed-file count combined. |

Ignored cache/build products are excluded by Git ignore rules. Binary untracked files are listed separately and receive no text-line count. Workspace-footprint fields are descriptive; they are not task thresholds or quality scores.

## Repeated-run interpretation

Each run should be analyzed independently before attempts are compared within a harness cell. Within-cell comparison may examine orientation depth, localization route, transformation mechanisms, recovery type, validation milestones, final workspace scope, and descriptive telemetry. Two runs can demonstrate route variation or recurrence, but they do not define a stable performance distribution.

Cross-harness conclusions should be made only after the relevant repeated-run cells are collected under the declared run protocol. Calls, tokens, cost, and elapsed time remain descriptive and are not combined into an overall score. Provider outage, environment startup failure, corrupted evidence, or operator interruption can invalidate a run; ordinary agent mistakes, verifier failure, or exhaustion of the predeclared agent budget do not.

## Reporting format

A per-run report should contain the verifier outcome, final workspace scope, orientation/localization route, lifecycle coordination route, Python extraction route, schema extraction route, verification sequence, recovery episodes, context-stewardship observations, and descriptive telemetry. Every route claim should be traceable to an observable action, result, workspace artifact, or verifier record.
