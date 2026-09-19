# Results and findings

## Canonical checkpoint

Version 0.1.0 contains 15 canonical Harbor runs: five Batchline tasks across OpenCode 1.18.30, Mini-SWE-Agent 2.4.6, and `custom-harness` snapshot-1. Every canonical run received `reward = 1.0` under the task/version shown below.

| Family | OpenCode | Mini-SWE | Custom harness |
|---|---:|---:|---:|
| B1 coordinated multi-file modification | 1.0 | 1.0 | 1.0 |
| R1 selective repeated edit | 1.0 | 1.0 | 1.0 |
| R2 large contiguous deletion | 1.0 | 1.0 | 1.0 |
| R3 large line-oriented inspection/filtering | 1.0 | 1.0 | 1.0 |
| R4 large contiguous move/module split | 1.0 | 1.0 | 1.0 |

The complete machine-readable matrix is available in [`results/batchline-focused/accepted-15/results.json`](results/batchline-focused/accepted-15/results.json), with CSV and Markdown forms in the same directory.

## Resource observations

The table below reproduces the main per-run resource fields from the canonical matrix. Calls, token totals, and cost are reported as observations from a single route; they are not combined into an efficiency score.

| Family | Harness | Task version | Reward | Calls | Input tokens | Cached | Output | Cost (USD) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| B1 | `opencode` | 0.1.0 | 1.0 | 11 | 121,055 | 100,352 | 1,398 | 0.0070 |
| B1 | `mini-swe-agent` | 0.1.0 | 1.0 | 20 | 143,568 | 112,640 | 3,356 | 0.0097 |
| B1 | `custom-harness` | 0.1.0 | 1.0 | 6 | 61,661 | 43,008 | 1,595 | 0.0048 |
| R1 | `opencode` | 0.1.0 | 1.0 | 14 | 139,027 | 116,736 | 1,205 | 0.0076 |
| R1 | `mini-swe-agent` | 0.1.0 | 1.0 | 12 | 63,336 | 36,864 | 962 | 0.0056 |
| R1 | `custom-harness` | 0.1.0 | 1.0 | 7 | 80,936 | 59,392 | 1,183 | 0.0055 |
| R2 | `opencode` | 0.1.1 | 1.0 | 16 | 296,787 | 258,048 | 1,218 | 0.0159 |
| R2 | `mini-swe-agent` | 0.1.1 | 1.0 | 31 | 337,441 | 276,480 | 4,224 | 0.0196 |
| R2 | `custom-harness` | 0.1.1 | 1.0 | 12 | 189,023 | 157,696 | 1,759 | 0.0102 |
| R3 | `opencode` | 0.1.1 | 1.0 | 4 | 30,906 | 18,432 | 300 | 0.0026 |
| R3 | `mini-swe-agent` | 0.1.1 | 1.0 | 16 | 84,284 | 51,200 | 3,092 | 0.0080 |
| R3 | `custom-harness` | 0.1.1 | 1.0 | 4 | 26,219 | 16,384 | 762 | 0.0023 |
| R4 | `opencode` | 0.1.0 | 1.0 | 13 | 207,203 | 176,128 | 2,861 | 0.0117 |
| R4 | `mini-swe-agent` | 0.1.0 | 1.0 | 22 | 334,192 | 288,768 | 7,233 | 0.0191 |
| R4 | `custom-harness` | 0.1.0 | 1.0 | 22 | 417,196 | 346,112 | 4,389 | 0.0229 |

The result JSON also records total elapsed time and agent execution time. Those timing fields are not reproduced here because test execution, validation depth, setup, and recovery work can materially affect wall-clock duration.

Two patterns are visible without turning them into rankings:

- Resource use is task-dependent rather than ordered consistently by harness. For example, Mini-SWE has fewer model calls and less input than OpenCode on R1, while OpenCode has a substantially shorter route on R3.
- The custom-harness rows have comparatively small call/input totals on B1, R1, and R3 and substantially larger totals on R4. With one canonical run per cell, that spread describes these executions rather than a stable performance distribution.

## Workspace observations

The public workspace observer records the final changed paths independently of correctness. The accepted OpenCode and Mini-SWE runs show both convergent and divergent solution scope.

| Family | OpenCode final scope | Mini-SWE final scope |
|---|---|---|
| B1 | 4 source files | 9 files: 4 source files, 4 tests, and `docs/concepts.md` |
| R1 | `config/job-policies.toml` only | `config/job-policies.toml` only |
| R2 | `README.md`, `providers.py`, provider tests | same three paths |
| R3 | `operations/quarantine-events.txt` only | `operations/quarantine-events.txt` only |
| R4 | `providers.py` plus new `legacy_remote.py` | `providers.py`, `execution/__init__.py`, plus new `legacy_remote.py` |

These scope differences are descriptive. B1 is the clearest example: both public harnesses satisfy the same contract, but Mini-SWE adds tests/documentation while OpenCode confines its final changes to the four product source files. The reward does not prefer one scope because the task does not impose an exact changed-file set.

The corresponding observer files are stored under [`evidence/public/`](evidence/public/).

## Public trajectory observations

The route analysis below is limited to OpenCode and Mini-SWE because those trajectories are included in the release.

### B1 — coordinated multi-file modification

OpenCode used structured repository search/read/edit operations to update the four required source surfaces, followed by validation. Mini-SWE used a shell-oriented workflow, inspected a wider set of repository tests, and left additional test/documentation changes in the final workspace.

Observed result: both approaches reach the same contract-correct outcome despite different final scope and tool substrate.

### R1 — selective repeated edit

OpenCode located the repeated `retry_policy` entries with structured search/read operations and applied contextual edits. Mini-SWE mapped the repeated entries through shell inspection and used line-addressed `sed` edits.

Observed result: the same three-entry configuration change was completed through visibly different editing abstractions, while both final workspaces contain only the requested configuration-file changes.

### R2 — large contiguous deletion

OpenCode began with structured reads/edits and entered a recovery path after an edit left the source in an invalid intermediate shape; it repaired the file with a script/shell route and then completed validation. Mini-SWE used shell-oriented inspection, deletion, test updates, and repeated repository checks. Both accepted runs ultimately changed the same three paths.

Observed result: similar final scope does not imply a similar interaction route. This task also demonstrates why trajectory evidence is useful for diagnosing recovery behavior without changing the correctness reward.

### R3 — large line-oriented inspection/filtering

OpenCode used a short route: inspect the archive size/sample, run a Python streaming/filter command, and read back the generated output. Mini-SWE performed broader repository exploration, inspected existing Batchline archive helpers/tests, cross-checked the filter behavior, and then produced the same output file.

Observed result: the accepted OpenCode route used 4 model calls while the accepted Mini-SWE route used 16, yet both final workspaces contain only the ten-line output artifact.

Possible interpretation: this may reflect different default workflow policies—direct artifact processing versus broader repository-oriented validation—but one run per harness is not enough to treat that difference as a stable harness property.

### R4 — large contiguous move/module split

OpenCode combined structured reads/writes/edits with shell-oriented operations for the large source move. Mini-SWE used a shell-centric extraction and verification route. Both created `legacy_remote.py`; Mini-SWE also updated `execution/__init__.py`.

Observed result: tool choice is not fixed solely by harness architecture. In the public OpenCode trajectories, structured operations dominate smaller localized edits, while larger movement/deletion tasks can trigger shell/script fallbacks.

## Verifier version notes

R2 and R3 use version 0.1.1 in the canonical matrix.

R2 v0.1.1 replaces an over-broad literal check with structural and behavioral deletion checks. This allows a valid negative regression test to mention `legacy_remote` while still requiring the implementation and registry entry to be removed.

R3 v0.1.1 keeps the solver instruction unchanged and computes expected event IDs with verifier-owned JSONL parsing. Archive integrity remains independently checked.

## Scope of conclusions

This release demonstrates that three harness configurations can satisfy the same five deterministic contracts while exhibiting materially different workspace scope and interaction routes. It does not establish a global ranking of coding agents or harnesses.

The current evidence is also too small for stable statistical claims about calls, token use, cost, or timing. Those fields are best read as route-level observations until repeated runs and broader task families are available.
