# Release artifacts

Agent Harness Smoke uses one canonical source tree for each release.

## GitHub source release

The version tag identifies the exact release tree. It contains the task/runtime/suite software, recorded results, published evidence, operational documentation, and active research layer. GitHub may expose automatically generated ZIP and tar archives for the tag.

## Zenodo archive

The Zenodo software record archives the same tagged source tree for persistent citation. A release archive should be generated from the final tag (for example with `git archive`) so it excludes `.git`, untracked working files, caches, and local build artifacts.

Release-to-release changes are recorded in the top-level `CHANGELOG.md`.
