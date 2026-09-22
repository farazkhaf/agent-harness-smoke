param(
    [string]$RepoRoot = "",
    [string]$SuitePath = "suites\batchline-scenario1\suite.toml",
    [string]$TrialsRoot = "",
    [string]$OutputRoot = "",
    [string[]]$TaskId = @(),
    [string[]]$ProfileId = @(),
    [switch]$PlanOnly,
    [switch]$KeepResolvedTask,
    [switch]$ContinueOnFailure
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

$runArgs = @{
    RepoRoot = $RepoRoot
    SuitePath = $SuitePath
    TaskId = $TaskId
    ProfileId = $ProfileId
    PlanOnly = $PlanOnly
    KeepResolvedTask = $KeepResolvedTask
    ContinueOnFailure = $ContinueOnFailure
}
if ($TrialsRoot) { $runArgs["TrialsRoot"] = $TrialsRoot }
if ($OutputRoot) { $runArgs["OutputRoot"] = $OutputRoot }

& (Join-Path $PSScriptRoot "run-suite.ps1") @runArgs
exit $LASTEXITCODE
