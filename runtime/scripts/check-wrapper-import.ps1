param(
    [string]$RepoRoot = ""
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$runtimeRoot = Join-Path $RepoRoot "runtime"

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$runtimeRoot;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $runtimeRoot
}

# Harbor was installed with `uv tool`.  UV_TOOL_BIN_DIR contains only the
# launcher/shim (`harbor.exe`); the tool's actual virtual environment lives
# under UV_TOOL_DIR\harbor.  Use that environment's Python for the import check.
$candidates = @()

if ($env:UV_TOOL_DIR) {
    $candidates += (Join-Path $env:UV_TOOL_DIR "harbor\Scripts\python.exe")
    $candidates += (Join-Path $env:UV_TOOL_DIR "harbor\bin\python")
}

# Portable fallback: ask uv for its tool directory when available.
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    $reportedToolDir = (& uv tool dir 2>$null | Select-Object -First 1)
    if ($reportedToolDir) {
        $candidates += (Join-Path $reportedToolDir "harbor\Scripts\python.exe")
        $candidates += (Join-Path $reportedToolDir "harbor\bin\python")
    }
}

$harborPython = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $harborPython) {
    $toolDir = if ($env:UV_TOOL_DIR) { $env:UV_TOOL_DIR } else { "<UV_TOOL_DIR is not set>" }
    throw "Could not locate Harbor's uv-tool Python environment. UV_TOOL_DIR=$toolDir. Tried: $($candidates -join ', ')"
}

$harborCommand = Get-Command harbor -ErrorAction Stop
Write-Host "Harbor launcher: $($harborCommand.Source)"
Write-Host "Harbor Python:   $harborPython"

& $harborPython -c "import harbor, sys; from harness_smoke_agents.preinstalled_mini_swe import PreinstalledMiniSweAgent; print('python=' + sys.executable); print('harbor=' + harbor.__file__); print('profile=' + PreinstalledMiniSweAgent.RUNTIME_PROFILE_ID)"
exit $LASTEXITCODE
