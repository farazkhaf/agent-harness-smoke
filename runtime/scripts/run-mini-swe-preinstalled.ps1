param(
    [string]$RepoRoot = "",
    [string]$TaskPath = "harness_smoke_phase1\prototype-task",
    [string]$Model = "fireworks_ai/accounts/fireworks/models/glm-5p3-flash",
    [switch]$KeepResolvedTask
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
& (Join-Path $RepoRoot "runtime\scripts\run-preinstalled.ps1") `
    -RepoRoot $RepoRoot `
    -TaskPath $TaskPath `
    -RuntimeProfile "runtime\profiles\mini-swe-2.4.6.yaml" `
    -Model $Model `
    -KeepResolvedTask:$KeepResolvedTask
exit $LASTEXITCODE
