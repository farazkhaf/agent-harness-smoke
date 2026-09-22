# Evidence and privacy

## Published run evidence

For each canonical OpenCode and Mini-SWE cell, including V1, the release includes:

- `run_receipt.json`, a sanitized summary of the Harbor result;
- `trajectory.json`, recording the public harness interaction route;
- `smoke_observation.json`, describing the final workspace scope;
- verifier stdout.

The run receipt omits host-local task and trial paths. It records SHA-256 hashes for the archived source result, the archived raw trajectory, and the published sanitized trajectory so that the curated evidence can be tied to the corresponding execution artifacts.

Trajectories are evidence for route-level analysis. They do not add hidden correctness requirements beyond the task verifier.

## Custom harness

The third harness is represented as `custom-harness` with version label `snapshot-1`. Its normalized correctness and resource fields are included in the 18-cell result matrix. Its implementation, prompts, tool schemas, adapters, and trajectory data are not distributed in this release. Route-level public findings therefore rely on the OpenCode and Mini-SWE evidence surface only; no public claim requires inspection of the private harness trajectory.

## Runtime artifacts

Raw Harbor trial directories, runtime databases, logs, snapshots, caches, local virtual environments, provider credentials, and host-specific absolute paths are not required to interpret the published matrix and are not included in the release package.

## Scenario 1 repeated-run evidence

Scenario 1 evidence is stored separately from the focused canonical matrix. Scenario 1 normalized summaries are stored under `results/batchline-scenarios/batchline-scenario1-v0.2.0-comparison/`; verifier-r1 and verifier-r2 result records remain for provenance, while verifier r3 is the current evaluator and does not change the recorded r2 outcomes. OpenCode and Mini-SWE attempts have public ATIF trajectories, sanitized run receipts, and verifier output under `evidence/public/scenario1/<harness>/attempt-<n>/`. The Mini-SWE timeout receipt retains only the exception type and timeout message; raw Harbor exception tracebacks and host-local paths are not published.

The custom Scenario 1 cell currently publishes sanitized receipts, neutral telemetry, and verifier-revision evidence but not the custom harness implementation, prompts, tool schemas, or raw trajectory. This keeps route-level research claims about the custom harness out of the public study unless a later normalized/redacted trace format is explicitly added.

The same evidence principle applies to later scenario cells: public route claims should be supported by the trajectory or workspace/verifier artifacts retained for that cell, and private-harness implementation details should not be required to reproduce public conclusions.
