# Release artifacts

Agent Harness Smoke uses one source tree with two release surfaces.

## Core package

The core package contains the reusable software/evaluation layer plus neutral reference evidence:

- `tasks/`, `runtime/`, and `suites/`;
- normalized `results/`;
- retained `evidence/`, including public trajectories where publishable and verifier revision history;
- product-facing `docs/`;
- root release/provenance files.

It excludes `research/`. A user can run, validate, or inspect prior executions without adopting the study interpretation.

## Study snapshot

The study snapshot contains the complete source tree, including `research/`. The research layer defines the formal study objective, research methods, and interpretive findings. It points back to the same tasks, results, and evidence rather than duplicating them.

Keeping the evidence shared is deliberate: trajectories and verifier records can be useful both as software-validation references and as research sources. The separation is between **neutral evidence** and **interpretation**, not between two incompatible copies of the executions.
