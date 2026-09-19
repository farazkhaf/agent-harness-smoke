# Task design — agent-harness-smoke/batchline-selective-retry-policies 0.1.0

## Purpose

This task changes `retry_policy` from `standard` to `aggressive` for exactly three named job kinds in Batchline's policy catalog.

The semantic requirement is explicit. The interaction pressure comes from selecting three target entries among 20 similar job tables without changing any other policy setting.

## Interaction focus

Primary interaction family: selective repeated edit.

The task can be solved with structured edits, line-oriented shell tools, scripted transformation, or another mechanism. Formatting and edit strategy are not correctness properties.

## Contract boundary

The verifier checks that:

- `thumbnail`, `billing_export`, and `daily_digest` use `aggressive`;
- every other job kind retains its existing retry policy;
- all other policy settings are semantically unchanged;
- the catalog continues to load and validate.

The verifier compares the semantic TOML document rather than an exact textual diff.
