# Task design — agent-harness-smoke/batchline-extract-legacy-remote-provider 0.1.0

## Purpose

This task moves Batchline's `LegacyRemoteProvider` implementation from the shared `providers.py` module into `legacy_remote.py` while preserving registration and behavior.

The semantic requirement is explicit. The interaction pressure comes from relocating a large source region, removing the original definition, creating the destination module, and reconnecting imports/registry behavior without introducing duplication or a proxy implementation.

## Interaction focus

Primary interaction family: large contiguous move/module split.

The task does not prescribe a copy, move, patch, shell, or structured-edit mechanism.

## Starting state

The task seed places shared execution request/plan/helper primitives in `execution/_common.py` while provider implementations, including the legacy provider, remain in `providers.py`. This keeps the extraction focused on source movement and module wiring rather than circular-import redesign.

## Contract boundary

The verifier checks that:

- the legacy provider implementation is loaded from `src/batchline/execution/legacy_remote.py`;
- `LegacyRemoteProvider` is no longer defined in `providers.py`;
- distinctive legacy-only implementation content is not duplicated in `providers.py`;
- `legacy_remote` remains registered;
- `get_provider("legacy_remote")` preserves representative behavior and defaults;
- current providers continue to work;
- the repository test suite passes.

The verifier does not require an exact class-body layout, method order, patch shape, or line count.
