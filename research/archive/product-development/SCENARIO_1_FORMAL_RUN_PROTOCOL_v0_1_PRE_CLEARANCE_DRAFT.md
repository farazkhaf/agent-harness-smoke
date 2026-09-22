# Scenario 1 Formal Run Protocol — v0.1

Status: **prospective freeze protocol**. This document must be fixed before the first formal solver run. If the task contract, verifier interpretation, anchor repository, or protocol changes materially after formal data collection starts, assign a new scenario version and restart the affected matrix rather than silently replacing earlier runs.

## 1. Scenario identity

- Task: `agent-harness-smoke/batchline-worker-draining-event-extraction`
- Freeze-candidate version: `0.1.0-rc1`
- Intended frozen version after Harbor author validation: `0.1.0`
- Anchor: `batchline` / `0.3-scenario1-seed`
- Scenario family: `S1`
- Primary research target: harness-mediated composition/friction under one fixed software target.

The task instruction, verifier, workspace observer, evaluation guide, anchor repository and author oracle freeze together.

## 2. Fixed harness/model cells

Use the same harness identities and underlying model family as the focused comparison whenever possible.

| Cell | Harness/version | Execution | Model/provider |
|---|---|---|---|
| O | OpenCode 1.18.30 | preinstalled Harbor runtime profile | Fireworks `accounts/fireworks/models/glm-5p3-flash` using OpenCode's native provider identifier |
| M | Mini-SWE-Agent 2.4.6 | preinstalled Harbor runtime profile | Fireworks `accounts/fireworks/models/glm-5p3-flash` using Mini-SWE/LiteLLM provider identifier |
| C | `custom-harness` snapshot-1 | external/private Harbor agent path used for the focused suite | Fireworks `accounts/fireworks/models/glm-5p3-flash` with the same private configuration used for the focused baseline |

Do not change model family, reasoning configuration, harness version or runtime image within a cell after formal collection starts. If a provider/runtime identifier differs only because a harness uses its native naming convention, record that explicitly rather than rewriting the harness's normal configuration.

## 3. Runtime/budget

Canonical task limits:

- agent timeout: **600 seconds**;
- verifier timeout: **180 seconds**;
- environment: **2 CPUs / 2048 MB**;
- task network requirement: **false**.

The scenario is not intended to be a timeout stress test. A solver-caused timeout inside these fixed limits is a run outcome, not a reason to substitute a cleaner repeat.

## 4. Prospective repeat policy

Schedule **three runs per harness cell** before observing Scenario 1 outcomes:

- O1, O2, O3;
- M1, M2, M3;
- C1, C2, C3.

Total planned formal solver runs: **9**.

All valid scheduled runs are retained. Do not request an extra run because a solver failure, long route, unusual tool choice, or high resource total looks inconvenient.

### Canonical narrative run

For detailed narrative trajectory review, the canonical run for each harness is **attempt 1** (O1/M1/C1), provided that attempt is formally valid. Attempts 2–3 remain first-class evidence for route/outcome variance and are not "diagnostic" replacements.

If attempt 1 is invalidated by a clear evaluator/infrastructure fault under Section 5, retain it in the record as invalid and use the prospectively scheduled replacement for the same attempt slot as the canonical narrative run. Never replace attempt 1 merely because another valid run is cleaner.

## 5. Valid run vs evaluator/infrastructure invalidation

Retain as solver/harness outcomes:

- reward 0;
- verifier-group failures or blocks caused by the final workspace;
- agent timeout;
- syntax/import/test failures introduced by the solver;
- route thrashing, repeated edits, or unsuccessful recovery;
- provider/harness errors that are plausibly part of the harness-mediated route rather than a confirmed external outage.

A run may be marked **invalid for formal comparison** only when there is concrete evidence of an external evaluation fault such as:

- task image/build/setup failure unrelated to solver actions;
- missing/incorrect evaluator files or verifier infrastructure failure in the unchanged package;
- credential/provider outage preventing the run from beginning meaningfully across the evaluation environment;
- corrupted/missing Harbor result artifacts due to runner failure;
- workspace observer/evidence collection failure caused by evaluator infrastructure when that makes the research dossier incomplete.

Invalid runs are retained and documented. A replacement run uses the same frozen cell/configuration. Invalidation must never be inferred solely from poor solver performance.

## 6. Correctness and evidence order

Inspect every run in this order:

1. Harbor binary reward;
2. named G1–G6 verifier-group artifact;
3. descriptive workspace observer artifact;
4. normalized telemetry;
5. trajectory review using the frozen Scenario 1 evaluation guide.

Only the verifier determines correctness. Workspace scope, tool choice, call count, token use, elapsed time and trajectory style are not hidden reward criteria.

## 7. Observer/verifier ordering

The canonical `tests/test.sh` must run the workspace observer **before** the verifier.

Required artifacts when supported by Harbor:

- `scenario_workspace_observation.json`;
- `scenario_verifier_groups.json`;
- Harbor reward/result files;
- ATIF/native trajectory where the harness exposes one under the project's evidence policy.

The observer remains descriptive. Extra/untracked files do not fail the task unless a separate explicit contract requirement makes them invalid.

## 8. Public suite and private cell execution

The public scenario suite schedules O1–O3 and M1–M3 from:

`suites/batchline-scenarios/suite.toml`

Use the generic runner:

```powershell
.\runtime\scripts\run-suite.ps1 `
  -SuitePath "suites\batchline-scenarios\suite.toml" `
  -TrialsRoot "$PWD\trials" `
  -OutputRoot "$PWD\results\batchline-scenario1\formal-v0.1"
```

The private/custom cell is executed separately through the existing external-agent path with the unchanged `custom-harness` snapshot-1 binding. Schedule exactly three attempts and normalize them into the same formal result set. Private harness implementation/import details need not enter the public artifact.

## 9. Prospective outcome summaries

With only three repeats per cell, use compact descriptive summaries rather than significance claims.

Report per harness:

- valid runs / planned runs;
- pass count and G1–G6 outcome frequencies;
- canonical-run dossier;
- distinct material route/recovery findings across repeats;
- median plus range/min–max for reliable calls/tokens/cost/timing fields;
- workspace-scope variation descriptively.

Do **not** convert these fields into an aggregate efficiency/friction score or rank harnesses overall.

## 10. Focused-to-scenario comparison boundary

Directly calibrated focused references:

- B1: coordinated multi-file modification;
- R4: substantial extraction/module integration.

Use those focused runs as contextual baselines for matched harness/model/version only. The focused suite has one canonical run per cell, so do not perform statistical focused-vs-scenario comparisons from those values.

Reference traversal, dependency-boundary reconciliation/import-cycle avoidance, schema compatibility work, recovery and context stewardship are scenario pressures without clean isolated focused baselines yet. They may nominate future focused tasks after Scenario 1 evidence is collected.

## 11. Trajectory-review discipline

Review each canonical trajectory against the frozen guide before writing cross-harness synthesis. Prefer reviewing one run at a time without using another harness's route as the expected solution sequence.

For each material finding record:

- concrete step/call evidence;
- direct observation;
- interpretation only where supported;
- alternative explanation/uncertainty;
- correctness/workspace/telemetry consequence if any.

Do not reward a solver for experiencing an avoidable error. Proactive avoidance of the known worker-event dependency/circular-import risk is a valid positive outcome.

## 12. Freeze gate before solver data collection

Promote `0.1.0-rc1` to `0.1.0` only after all of the following pass on a Harbor-capable host:

1. canonical standalone task builds;
2. Harbor NOP gives reward 0 and expected diagnostic group vector;
3. Harbor Oracle gives reward 1 with G1–G6 pass;
4. observer artifact exists and is produced before verifier execution;
5. named verifier-group artifact is preserved in trial artifacts;
6. OpenCode 1.18.30 runtime binding resolves/builds unchanged canonical task;
7. Mini-SWE-Agent 2.4.6 runtime binding resolves/builds unchanged canonical task;
8. runtime/reporting path preserves scenario group and observer diagnostics;
9. frozen suite plan expands to exactly 3 attempts per public cell;
10. task package checksum/version and protocol are recorded before O1/M1/C1 begin.

After this gate, solver-facing changes require a new task version and prospective matrix restart.
