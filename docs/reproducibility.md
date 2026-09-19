# Reproducibility

## Requirements

The public runners assume a Harbor-capable environment with Docker and PowerShell. The release pins the two public harness profiles used for the canonical comparison:

- Mini-SWE-Agent 2.4.6
- OpenCode 1.18.30

The task packages are agent-agnostic. Repository dependencies are installed by each task's `environment/setup/setup.sh`; harness installation is kept in reusable preinstalled runtime images.

## Build public harness runtimes

```powershell
.\runtime\scripts\build-mini-swe-runtime.ps1
.\runtime\scripts\build-opencode-runtime.ps1
```

## Preview the focused matrix

```powershell
.\runtime\scripts\run-focused-suite.ps1 -PlanOnly
```

## Run the focused matrix

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TrialsRoot "$PWD\trials"
```

`trials/` is the raw Harbor execution store. Normalized output is written under `results/batchline-focused/`.

Selected cells can be run with `-TaskId` and `-ProfileId`:

```powershell
.\runtime\scripts\run-focused-suite.ps1 `
  -TaskId "agent-harness-smoke/batchline-selective-retry-policies" `
  -ProfileId "opencode-1.18.30" `
  -TrialsRoot "$PWD\trials"
```

## Normalize an existing trial

```powershell
.\runtime\scripts\report-trial.ps1 `
  -TrialPath "$PWD\trials\<trial-folder>"
```

The reporter writes normalized JSON, Markdown, and CSV output under the trial's `smoke-report/` directory.

## Collect normalized reports

```powershell
.\runtime\scripts\collect-focused-suite.ps1 `
  -ReportsRoot "results\batchline-focused\<run>"
```

## Release evidence

The canonical 15-cell matrix is stored under `results/batchline-focused/accepted-15/`. Curated run evidence for the ten OpenCode and Mini-SWE cells is stored under `evidence/public/`.

See [evidence_and_privacy.md](evidence_and_privacy.md) for the fields and artifacts included in the published evidence set.
