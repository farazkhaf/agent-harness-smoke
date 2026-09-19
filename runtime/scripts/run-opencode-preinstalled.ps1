param(
    [string]$RepoRoot = "",
    [string]$TaskPath = "harness_smoke_phase1\prototype-task",
    [string]$Model = "fireworks-ai/accounts/fireworks/models/glm-5p3-flash",
    [switch]$KeepResolvedTask
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
if (-not $env:FIREWORKS_API_KEY -and -not $env:FIREWORKS_AI_API_KEY) {
    throw "Set FIREWORKS_API_KEY or FIREWORKS_AI_API_KEY in the Harbor shell before running OpenCode."
}

& (Join-Path $RepoRoot "runtime\scripts\run-preinstalled.ps1") `
    -RepoRoot $RepoRoot `
    -TaskPath $TaskPath `
    -RuntimeProfile "runtime\profiles\opencode-1.18.30.yaml" `
    -Model $Model `
    -KeepResolvedTask:$KeepResolvedTask
exit $LASTEXITCODE
