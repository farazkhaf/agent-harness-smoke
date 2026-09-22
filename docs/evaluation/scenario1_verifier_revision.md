# Scenario 1 verifier revisions

Scenario 1 keeps solver-visible task version `0.2.0`. Verifier revisions modify only the external evaluator; they do not change the instruction, seed repository, runtime environment, task metadata, observer, test wrapper, oracle solution, model configuration, or any recorded agent execution.

## Revision 1 — collection-time evaluator

Revision 1 was used for the original six recorded executions. It required the five canonical worker names to be absent from aggregate `$defs` and required aggregate worker variants to use one direct external-reference layout.

Custom Attempt 1 instead used pure local forwarding aliases: the aggregate `$defs` entries contained only external `$ref` forwarding, while the concrete worker schemas lived in `worker-events.schema.json`. Revision 1 therefore recorded a G5-only failure.

## Revision 2 — contract correction

The solver-visible instruction required **concrete worker schema ownership** to move to the dedicated worker schema, but did not prohibit pure forwarding aliases or prescribe one canonical reference layout. Revision 2 evaluates ownership rather than syntax:

- direct external worker variants are accepted;
- pure local forwarding aliases are accepted;
- local worker schema assertions remain rejected;
- the dedicated worker schema must still contain all required concrete definitions.

The same audit removed three smaller implementation assumptions: registry transitions no longer require Python object identity; legacy heartbeat compatibility is tested behaviorally rather than by freezing one fixture shape; and independent schema loadability is checked as JSON-Schema validity rather than requiring standalone event validation without reference resolution.

### Custom Attempt 1 adjudication

The original r1 result is retained as historical evidence. The Attempt-1 workspace was reconstructed from its preserved trajectory and first reproduced the original r1 outcome exactly: G1-G4 and G6 passed, G5 failed. The identical workspace then passed G1-G6 under r2. No agent was rerun.

The result change is therefore attributed to an evaluator-contract correction, not to a second solution attempt or special treatment of the custom harness.

## Revision 3 — regression hardening

Revision 3 preserves r2's acceptance behavior while making two explicit contract checks robust to imagined edge implementations:

1. A concrete worker event schema retained in aggregate `$defs` is rejected even if its definition name is changed. Ownership is detected from the worker `event_type` assertion rather than only the five canonical definition names.
2. Registry drain/resume checks explicitly verify that both returned and stored snapshots preserve the identity, service, queue, heartbeat timestamp, active-job count, and physical capacity fields named by the instruction. Object identity is still not required.

Revision 3 does **not** require a direct external worker `oneOf` item to be a bare `$ref`. A direct external `$ref` with a harmless sibling such as `"type": "object"` remains valid.

No recorded Scenario 1 workspace contains either r3 edge condition, so the six recorded outcomes are unchanged from r2.

## Revision history

| Harness | Attempt | r1 | r2 | r3 outcome |
|---|---:|---|---|---|
| OpenCode 1.18.30 | 1 | pass | pass | pass |
| OpenCode 1.18.30 | 2 | pass | pass | pass |
| Mini-SWE-Agent 2.4.6 | 1 | G1 fail | G1 fail | G1 fail |
| Mini-SWE-Agent 2.4.6 | 2 | pass | pass | pass |
| custom-harness | 1 | G5 fail | pass | pass |
| custom-harness | 2 | pass | pass | pass |

The exact verifier sources, SHA-256 records, and diffs are preserved under `evidence/verifier-revisions/scenario1-v0.2.0/`.
