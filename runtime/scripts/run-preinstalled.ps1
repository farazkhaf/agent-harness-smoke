param(
    [string]$RepoRoot = "",
    [Parameter(Mandatory = $true)][string]$TaskPath,
    [Parameter(Mandatory = $true)][string]$RuntimeProfile,
    [Parameter(Mandatory = $true)][string]$Model,
    [string]$TrialsRoot = "",
    [int]$AgentSetupTimeout = 300,
    [switch]$KeepResolvedTask
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$runtimeRoot = Join-Path $RepoRoot "runtime"
if (-not $TrialsRoot) {
    $TrialsRoot = Join-Path $RepoRoot "trials"
} elseif (-not [System.IO.Path]::IsPathRooted($TrialsRoot)) {
    $TrialsRoot = Join-Path $RepoRoot $TrialsRoot
}
New-Item -ItemType Directory -Force -Path $TrialsRoot | Out-Null

if (-not [System.IO.Path]::IsPathRooted($TaskPath)) {
    $TaskPath = Join-Path $RepoRoot $TaskPath
}
if (-not [System.IO.Path]::IsPathRooted($RuntimeProfile)) {
    $RuntimeProfile = Join-Path $RepoRoot $RuntimeProfile
}

$taskName = Split-Path $TaskPath -Leaf
$profileName = [System.IO.Path]::GetFileNameWithoutExtension($RuntimeProfile)
$resolvedRoot = Join-Path ([System.IO.Path]::GetTempPath()) "harbor-smoke-resolved"
$resolvedTask = Join-Path $resolvedRoot ("{0}--{1}--{2}" -f $taskName, $profileName, [guid]::NewGuid().ToString("N"))
$exitCode = 1
New-Item -ItemType Directory -Force -Path $resolvedRoot | Out-Null

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$runtimeRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $runtimeRoot
}

try {
    python (Join-Path $runtimeRoot "bind_task.py") `
        --task $TaskPath `
        --profile $RuntimeProfile `
        --output $resolvedTask
    if ($LASTEXITCODE -ne 0) { throw "Task/runtime binding failed." }

    $bindingPath = Join-Path $resolvedTask ".harness-smoke-binding.json"
    $binding = Get-Content -Raw $bindingPath | ConvertFrom-Json

    Write-Host ("Resolved {0} with {1} -> {2}" -f $taskName, $binding.runtime_profile_id, $resolvedTask)
    Write-Host ("Runtime image: {0}" -f $binding.runtime_image)

    harbor trial start `
      -p $resolvedTask `
      -a $binding.integration `
      -m $Model `
      --agent-setup-timeout $AgentSetupTimeout `
      --trials-dir $TrialsRoot
    $exitCode = $LASTEXITCODE
}
finally {
    if (-not $KeepResolvedTask -and (Test-Path $resolvedTask)) {
        Remove-Item -Recurse -Force $resolvedTask
    } elseif ($KeepResolvedTask -and (Test-Path $resolvedTask)) {
        Write-Host "Kept resolved task: $resolvedTask"
    }
}

exit $exitCode
