param(
    [string]$RepoRoot = "",
    [Parameter(Mandatory = $true)][string]$TaskPath,
    [Parameter(Mandatory = $true)][string]$Agent,
    [string]$Model = "",
    [string]$TrialsRoot = ""
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

if (-not $TrialsRoot) {
    $TrialsRoot = Join-Path $RepoRoot "trials"
} elseif (-not [System.IO.Path]::IsPathRooted($TrialsRoot)) {
    $TrialsRoot = Join-Path $RepoRoot $TrialsRoot
}
New-Item -ItemType Directory -Force -Path $TrialsRoot | Out-Null

if (-not [System.IO.Path]::IsPathRooted($TaskPath)) {
    $TaskPath = Join-Path $RepoRoot $TaskPath
}

if (-not (Test-Path $TaskPath)) {
    throw "Canonical task not found: $TaskPath"
}

# External Harbor agents stay in the host Harbor process and interact with the
# canonical task environment through Harbor's BaseEnvironment interface. The
# agent import path must already be importable by the Harbor Python process
# (for example via an installed package or the caller's PYTHONPATH).
$argsList = @("trial", "start", "-p", $TaskPath, "--agent", $Agent, "--trials-dir", $TrialsRoot)
if ($Model) {
    $argsList += @("-m", $Model)
}

Write-Host ("Running external Harbor agent {0} on canonical task {1}" -f $Agent, $TaskPath)
if ($Model) {
    Write-Host ("Harbor-managed model: {0}" -f $Model)
} else {
    Write-Host "Harbor-managed model: <none; external agent owns model/provider configuration>"
}

& harbor @argsList
exit $LASTEXITCODE
