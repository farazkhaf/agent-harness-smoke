# Evidence and privacy

## Published run evidence

For each canonical OpenCode and Mini-SWE cell, the release includes:

- `run_receipt.json`, a sanitized summary of the Harbor result;
- `trajectory.json`, recording the public harness interaction route;
- `smoke_observation.json`, describing the final workspace scope;
- verifier stdout.

The run receipt omits host-local task and trial paths. It records SHA-256 hashes for the archived source result, the archived raw trajectory, and the published sanitized trajectory so that the curated evidence can be tied to the corresponding execution artifacts.

Trajectories are evidence for route-level analysis. They do not add hidden correctness requirements beyond the task verifier.

## Custom harness

The third harness is represented as `custom-harness` with version label `snapshot-1`. Its normalized correctness and resource fields are included in the 15-cell result matrix. Its implementation, prompts, tool schemas, adapters, and trajectory data are not distributed in this release.

## Runtime artifacts

Raw Harbor trial directories, runtime databases, logs, snapshots, caches, local virtual environments, provider credentials, and host-specific absolute paths are not required to interpret the published matrix and are not included in the release package.
