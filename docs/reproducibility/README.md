# Reproducibility

## Requirements

The bundled PowerShell runners assume Harbor, Docker, Python, and PowerShell. The included reference runtime profiles are Mini-SWE-Agent 2.4.6 and OpenCode 1.18.30. Tasks themselves remain agent-agnostic.

To add another harness, see [`adding_harnesses.md`](adding_harnesses.md).

## Build the included preinstalled runtimes

```powershell
.\runtime\scripts\build-mini-swe-runtime.ps1
.\runtime\scripts\build-opencode-runtime.ps1
```

## Focused suite

Preview:

```powershell
.\runtime\scripts\run-focused-suite.ps1 -PlanOnly
```

Run:

```powershell
.\runtime\scripts\run-focused-suite.ps1 -TrialsRoot "$PWD\trials"
```

Selected tasks or profiles can be run with `-TaskId` and `-ProfileId`.

The recorded focused checkpoint is stored under `results/batchline-focused/accepted-18/`. Public OpenCode and Mini-SWE run evidence is stored under `evidence/public/`.

## Scenario 1

Scenario 1 uses `suites/batchline-scenario1/suite.toml` and the convenience runner:

```powershell
.\runtime\scripts\run-scenario1.ps1 -ProfileId opencode-1.18.30
.\runtime\scripts\run-scenario1.ps1 -ProfileId mini-swe-2.4.6
```

The task declares a 600-second agent timeout and a 180-second verifier timeout. Scenario output defaults to `results\batchline-scenarios\<suite-id>\<timestamp>` when no output root is supplied.

## Normalize an existing trial

```powershell
.\runtime\scripts\report-trial.ps1 -TrialPath "$PWD\trials\<trial-folder>"
```

The reporter writes normalized JSON, Markdown, and CSV under the trial's `smoke-report/` directory. Suite-level collectors aggregate those normalized reports without requiring the raw trial to be republished.

See [`evidence_and_privacy.md`](evidence_and_privacy.md) for the curated evidence surface.
