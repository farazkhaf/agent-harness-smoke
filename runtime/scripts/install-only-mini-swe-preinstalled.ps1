param(
    [string]$RepoRoot = "",
    [string]$Model = "fireworks_ai/accounts/fireworks/models/glm-5p3-flash"
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$runtimeRoot = Join-Path $RepoRoot "runtime"
$taskPath = Join-Path $RepoRoot "harness_smoke_phase1\prototype-task-mini-swe"

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$runtimeRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $runtimeRoot
}

harbor run `
  -p $taskPath `
  -a "harness_smoke_agents.preinstalled_mini_swe:PreinstalledMiniSweAgent" `
  -m $Model `
  --install-only `
  --agent-setup-timeout-multiplier 2 `
  --n-concurrent 1
exit $LASTEXITCODE
