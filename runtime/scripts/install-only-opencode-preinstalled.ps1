param(
    [string]$RepoRoot = "",
    [string]$Model = "fireworks-ai/accounts/fireworks/models/glm-5p3-flash"
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$runtimeRoot = Join-Path $RepoRoot "runtime"
$taskPath = Join-Path $RepoRoot "harness_smoke_phase1\prototype-task-opencode"

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$runtimeRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $runtimeRoot
}

if (-not $env:FIREWORKS_API_KEY -and -not $env:FIREWORKS_AI_API_KEY) {
    throw "Set FIREWORKS_API_KEY or FIREWORKS_AI_API_KEY in the Harbor shell before running OpenCode."
}

harbor run `
  -p $taskPath `
  -a "harness_smoke_agents.preinstalled_opencode:PreinstalledOpenCode" `
  -m $Model `
  --install-only `
  --agent-setup-timeout-multiplier 2 `
  --n-concurrent 1
exit $LASTEXITCODE
