# Scenario 1 repeated-run findings

Scenario 1 studies a coordinated worker lifecycle change that also extracts Python event construction and worker JSON-Schema ownership. This document records trajectory-supported findings from the retained Scenario 1 runs.

## Recorded configuration

Task: `agent-harness-smoke/batchline-worker-draining-event-extraction` version `0.2.0`.

The recorded runs use GLM-5.3-Flash with a 600-second agent timeout and no additional per-harness token, step, or cost cap. OpenCode 1.18.30 and Mini-SWE-Agent 2.4.6 omit `reasoning_effort`, which GLM-5.3-Flash documents as defaulting to `max`; the custom Scenario 1 profile uses explicit `max`. Each harness cell contains two independent runs.

The recorded matrix contains two runs each for OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and the custom harness. Results use the current verifier (`r3`); the collection-time verifier is retained as provenance because it originally rejected one custom-harness workspace under an overconstrained schema-reference check. No agent execution was repeated for that correction.

OpenCode and Mini-SWE route analysis is supported by published trajectories. Custom-harness results are reported through outcome and run telemetry because its raw trajectory remains private. Verifier history is documented in [`docs/provenance/scenario1_verifier_history.md`](../../docs/provenance/scenario1_verifier_history.md).

## OpenCode 1.18.30: two-run cell

Both OpenCode runs satisfy all six verifier groups with `reward = 1.0`.

| Attempt | Verifier | Total changed files | Text lines added | Text lines deleted | Inference calls | Uncached input | Output tokens | Agent execution |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.0 | 14 | 677 | 381 | 45 | 111,053 | 12,906 | 378.9 s |
| 2 | 1.0 | 14 | 639 | 365 | 42 | 95,228 | 11,928 | 307.2 s |

The two accepted workspaces are similar in scope but not identical in physical footprint. These values describe the observed routes; two samples are not sufficient for a stable efficiency distribution.

### Attempt 1

Trajectory: `evidence/public/scenario1/opencode/attempt-1/trajectory.json`.

Steps 2-14 are primarily orientation and integration planning. The run uses native reads for source and test files, but shell inspection for some small JSON examples. The 847-line aggregate schema is read through the native read operation, so this run does not provide evidence of capped/continuation traversal for that file. At step 13 the agent performs a small isolated `jsonschema`/`referencing` experiment before implementation, confirming that a registry can resolve a sibling worker schema.

Workspace edits begin at step 15. The worker lifecycle, registry, serializer, rendering, CLI, shared event support, and worker event module are changed incrementally. The initial `encoder.py` edit at step 21 updates the header/import structure but leaves the old worker constructor bodies in place. At steps 22-24 the agent notices the incomplete transformation, rereads the affected region, and switches to a Python text transformation that removes the constructor block and repairs shared helper references. This is an incomplete-transformation/edit-route correction rather than a failed edit tool call.

The large aggregate-schema removal is handled structurally. After selective `$ref` edits, step 30 parses `events.schema.json`, removes the four worker definitions by key, asserts the removed titles, and serializes the preserved schema. This is a parse-transform-serialize route rather than a large text-range deletion.

By step 34 the repository test suite and event-example validation are green. The next temporary smoke script contains an incorrect assertion: it expects a draining worker's table `LOAD` to become `0/4`, although the contract preserves `active_jobs/capacity` and only sets `available_slots` to zero. Steps 35-41 are spent localizing this self-authored verification error. The agent first probes rendering directly, then writes the long smoke check to `/tmp` to obtain an exact traceback line, confirms the draining row is correctly `1/4`, fixes only the temporary assertion, and reruns the smoke script successfully. No repository product file changes result from this episode.

The full repository `make check` succeeds at step 42, followed by final status/diff review and auxiliary workflow checks. The late smoke episode is therefore best characterized as verification-localization overhead around a solver-authored check, not implementation recovery.

Context-stewardship observations from this attempt are mixed but informative. The early cross-schema spike reduces uncertainty before the integration edit. Later, the run externalizes a long temporary probe into a file to improve line-level diagnosis, which is a useful localization technique. At the same time, the mistaken assertion creates several additional calls after substantial correctness evidence was already available. Both behaviors should be retained in the analysis rather than collapsed into a generic error count.

### Attempt 2

Trajectory: `evidence/public/scenario1/opencode/attempt-2/trajectory.json`.

Steps 2-14 again map the worker, event, schema, CLI, serializer, test, and repository-validation surfaces. Edits begin at step 15. Unlike Attempt 1, this run rewrites `encoder.py` directly at step 23 into its intended final ownership structure instead of first attempting a partial extraction. The aggregate schema follows a similar structured route to Attempt 1: worker `$ref`s are edited selectively, then step 28 parses the JSON schema and deletes the worker definitions by key.

This attempt performs less isolated preflight around the `referencing` API. Its first integrated smoke check exposes a genuine implementation error in `validation.py`: `Resource.id` was treated as a value rather than the method `Resource.id()`. Steps 33-34 inspect the library object and make a targeted product-code repair. The corrected smoke check succeeds at step 35.

The repository test suite passes at step 36, and event/config/policy validation succeeds at step 37. The run then performs targeted edge checks for interleaved event IDs, legacy construction, drain validation, registry capacity, CLI output, serializer behavior, standalone worker-schema validation, and legacy heartbeat compatibility. A complete `make check` is green at step 40; the remaining actions are final validation and review.

This recovery should be coded as an execution-discovered implementation/integration defect with targeted API inspection. It differs materially from Attempt 1's temporary smoke assertion error.

### Within-cell observations

The two runs reach the same verifier outcome through visibly different routes.

| Dimension | Attempt 1 | Attempt 2 |
|---|---|---|
| External-schema uncertainty | Isolated compatibility spike before implementation | Resolved after integrated execution exposed an API mistake |
| `encoder.py` extraction | Incremental edit, incomplete transformation detected, then script-assisted removal | Whole-file rewrite to the intended ownership structure |
| Aggregate JSON-schema removal | Structured parse-transform-serialize | Structured parse-transform-serialize |
| Main recovery episode | Temporary verification assertion was wrong | Product integration used `Resource.id` incorrectly |
| Product edits caused by main recovery | None | Targeted `validation.py` edit |
| Final verifier | Pass | Pass |

The shared schema-removal route is notable because the task does not prescribe JSON parsing. Both runs independently chose a structural transformation for the large preservation-sensitive edit. The Python extraction, by contrast, shows within-harness route variation.

Inspection route should not be inferred from file extension. Attempt 1 uses shell `cat` for small JSON examples while reading the much larger JSON Schema through the native read operation. The useful research categories are the interaction primitives themselves—native read, range/continuation read, shell inspection, search, and structured parse/query—not a rule such as "JSON uses shell".

The cell also demonstrates why recovery type matters. Attempt 1 spends several late calls diagnosing a wrong temporary assertion while the repository implementation remains correct; Attempt 2 repairs a real integration defect. Treating both as a single retry count would erase a meaningful difference in context stewardship and recovery behavior.

## Mini-SWE-Agent 2.4.6: two-run cell

The Mini-SWE cell contains one accepted run and one valid failing run. Both execute through the same Bash-only agent interface and the same 600-second agent timeout. The failing attempt is retained rather than replaced: Harbor records a normal sequence of model calls and shell executions until the declared agent budget is exhausted, and the post-timeout verifier identifies a remaining product defect.

| Attempt | Verifier | Total changed files | Text lines added | Text lines deleted | Inference calls | Uncached input | Output tokens | Agent execution |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.0 | 14 | 802 | 383 | 47 | 104,467 | 60,210 | 600.0 s |
| 2 | 1.0 | 14 | 700 | 380 | 43 | 92,928 | 44,405 | 426.6 s |

### Attempt 1

Trajectory: `evidence/public/scenario1/mini-swe-agent/attempt-1/trajectory.json`.

The run spends calls 1-19 primarily on orientation. Because Mini-SWE executes through a fresh-shell Bash interface, it repeatedly establishes `/app` explicitly and often concatenates several logical files into one observation. The harness formats shell output above 10,000 characters as a 5,000-character head plus 5,000-character tail; this occurs twice during this run. These are interface conditions rather than errors, but they make artifact boundaries and omitted middle content part of the model's context-management burden.

At call 19 the run writes a temporary verification script; the first product edit follows at call 20 (trajectory step 22). Before implementation, the reasoning explicitly states both sides of the `WorkerSnapshot` state invariant: a non-draining worker must have no drain reason, while a draining worker must have a non-empty reason. The implementation nevertheless enforces only the second half. The omitted non-draining-with-reason rejection persists to the final workspace and is the verifier's sole failing group: G1 fails while G2-G6 pass. This is evidence of requirement loss across a long multi-surface transformation rather than failure to discover the requirement.

The run's temporary verification does not exercise the omitted invariant. It therefore continues through registry, public surfaces, event extraction, schema extraction, registry/schema parity, example updates, and repository validation without rediscovering the defect. This distinction matters for context stewardship: the requirement was represented during planning but was not preserved into either the implementation or the solver-authored verification surface.

By steps 43-44, the repository's own 55 tests, example validation, and `make check` are green. The run nevertheless continues changing schema representation and `validation.py` through steps 45-48, including restructuring aggregate worker references, revising event-type traversal, and removing a helper introduced during the same run. Step 49 again reports passing native tests, the temporary verification, and repository checks. The agent has not issued its completion/submission action when Harbor terminates execution at the declared 600-second agent budget.

The timeout is therefore coded as a valid run outcome, not an infrastructure invalidation. The retained sanitized receipt records `AgentTimeoutError: Agent execution timed out after 600.0 seconds`; provider calls and shell actions continued normally before termination, and the verifier subsequently found the remaining G1 defect.

### Attempt 2

Trajectory: `evidence/public/scenario1/mini-swe-agent/attempt-2/trajectory.json`.

This run begins product edits substantially earlier, at trajectory step 12 (agent call 10), after a shorter orientation phase. It uses the same shell-only interface and also triggers the harness's long-output head/tail elision twice, so shell aggregation alone does not determine the final outcome.

The route remains iterative. The run creates shared event-construction support and rewrites `encoder.py`, then builds the worker schema and aggregate-schema changes. While rewriting `validation.py`, it temporarily omits `load_event_schema`, then `EventValidationError`, and later repairs `schema_event_types()` semantics after execution exposes the mismatch. These are execution-discovered implementation/integration defects, not provider failures. The run also encounters a missing `xxd` command during a formatting check; the command issue does not affect the repository state.

The important difference from Attempt 1 is convergence. The lifecycle invariant is implemented completely, successive execution feedback is incorporated into the product, and the repository reaches repeatable green checks within the common budget. `make check` passes at step 43; step 44 runs a final comprehensive verification and workspace review, and step 45 reaches the harness completion action. The post-run verifier passes G1-G6 with reward 1.0.

### Mini-SWE cell observations

The two runs support a narrower claim than “shell-only agents fail.” Both runs share the same Bash-only interaction model, fresh-shell command state, and long-output elision policy, yet one satisfies the contract. The relevant evidence is how the model manages that interface.

The failing attempt performs substantially more pre-edit exploration, loses one already-articulated lifecycle invariant during implementation, omits the same invariant from its temporary verification, and continues post-green restructuring until the global execution budget is exhausted. The accepted attempt starts implementation earlier and repairs several self-induced integration defects before the budget boundary.

Shell composition creates additional interaction hazards worth recording. Concatenating multiple files can collapse logical artifact boundaries into a single observation, and pipelines such as `python ... | tail` can report the status of the final pipeline command unless pipe failure is propagated. These properties are not scored as errors by themselves; they are part of the interaction substrate whose management is observable in the trajectory.

The cell therefore provides evidence of an unstable completion boundary for Mini-SWE-Agent 2.4.6 on this scenario under the declared 600-second budget: one of two runs completes and passes, while the other reaches the budget after 47 model calls with one lifecycle invariant still unsatisfied. With two samples this should not be generalized into a harness-wide failure rate or ranking.


## Custom harness: two-run cell

The custom harness recorded two Scenario 1 runs with the same GLM-5.3-Flash model at explicit `reasoning_effort=max`. Attempt 1 used 25 inference calls, 92,051 uncached input tokens, 12,697 non-reasoning output tokens, 20,324 reasoning tokens, and 304.5 seconds of agent execution; Attempt 2 used 32 calls, 100,287 uncached input tokens, 16,567 non-reasoning output tokens, 19,495 reasoning tokens, and 340.1 seconds. Both changed 14 workspace paths. These measurements describe the recorded executions; the harness exposes a different interaction interface and its raw trajectory is not published.

Custom Attempt 1 was rejected by the collection-time verifier because the aggregate schema retained pure forwarding aliases to definitions owned by `worker-events.schema.json`. The task contract required concrete worker-schema ownership to move to the dedicated schema but did not prohibit that forwarding layout. The current verifier evaluates ownership by substantive schema assertions rather than by one canonical reference shape, so the unchanged workspace passes G1-G6. The original result and verifier are retained as provenance.

This correction is evaluator history, not an additional agent attempt. It also differs from Mini-SWE Attempt 1, whose current workspace still violates the explicit lifecycle invariant checked by G1.

Because the custom trajectory is private, current public findings do not attribute specific route mechanisms to that harness. Its outcome and telemetry remain useful as black-box execution evidence.

## Current scope of interpretation

Scenario 1 now contains three two-run harness cells under one fixed software target and model family. Under the current verifier, OpenCode and the custom harness each have two passing recorded workspaces; Mini-SWE has one pass and one valid failing timeout run with an unchanged G1 lifecycle defect. These counts describe the retained observations.

The evidence is intended for mechanism-level study: inspection and transformation primitives, route choice, requirement retention, recovery causes, context stewardship, verification behavior, affordance uptake, and completion boundaries. Two runs per harness can demonstrate recurrence or variation in observed routes but do not estimate stable success probabilities.

OpenCode and Mini-SWE route claims are supported by retained public trajectories. Custom-harness conclusions remain at the black-box outcome and telemetry level in the current evidence package.
