# Task design — agent-harness-smoke/batchline-submitted-by 0.1.0

## Purpose

This task tests coordinated propagation of one explicit product change across several existing repository surfaces. Batchline jobs gain optional `submitted_by` metadata, and that value must survive job construction/mapping and appear through the specified API and CLI representations.

The semantic requirement is intentionally straightforward. The interaction pressure comes from locating the relevant model, service, serializer, and CLI code and keeping the resulting repository state mutually consistent.

## Interaction focus

Primary interaction family: coordinated multi-file source modification.

The task can expose differences in repository orientation, cross-file context management, edit reliability, and verification workflow. It does not prescribe search, shell, structured editing, patching, or any other tool mechanism.

## Contract boundary

The verifier checks the stated behavior:

- jobs can carry optional `submitted_by` metadata;
- service submission accepts and preserves the value;
- mapping construction preserves the value;
- API serializers expose the required key/value behavior;
- CLI detail rendering shows the value or the specified fallback;
- existing calls and jobs that omit the field continue to work.

The verifier does not require an exact patch, exact line placement, a fixed changed-file set, added tests/documentation, or a particular command sequence.

## Interpretation

A pass means the final workspace satisfies the multi-surface compatibility contract. Workspace scope and trajectory evidence may be used to compare how different harnesses reached that state, but they do not change the reward unless a task requirement explicitly makes them part of correctness.
