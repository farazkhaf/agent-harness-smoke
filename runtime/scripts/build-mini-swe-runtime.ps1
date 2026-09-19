param(
    [string]$RepoRoot = "",
    [string]$Image = "harness-smoke/mini-swe:2.4.6"
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$dockerContext = Join-Path $RepoRoot "runtime\images\mini-swe"

Write-Host "Building $Image from $dockerContext"
docker build --progress=plain -t $Image $dockerContext
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Runtime image built. Verifying installed agent..."
docker run --rm $Image sh -lc "command -v mini-swe-agent && uv tool list | grep '^mini-swe-agent ' && mini-swe-agent --help >/dev/null"
exit $LASTEXITCODE
