# Task design — agent-harness-smoke/batchline-remove-legacy-remote-provider 0.1.1

## Purpose

This task removes Batchline's deprecated `legacy_remote` execution provider and the positive compatibility coverage that exists only for that provider while preserving all current providers.

The semantic requirement is explicit. The main interaction pressure is a substantial contiguous deletion in a shared source module together with the associated registry and test cleanup.

## Interaction focus

Primary interaction family: large contiguous deletion.

The task does not prescribe a deletion tool, patch form, line range, or editing mechanism.

## Contract boundary

The verifier checks that:

- `LegacyRemoteProvider` is no longer defined;
- `legacy_remote` is absent from the provider registry;
- no compatibility stub or alias replaces it;
- stale positive compatibility coverage is removed;
- current providers remain registered and functional;
- the repository test suite passes.

Negative regression coverage that mentions `legacy_remote` while asserting rejection is valid.

## Version note

Version 0.1.1 replaces an over-broad verifier check from 0.1.0 with structural and behavioral checks that allow valid negative regression tests. The task instruction is unchanged.
