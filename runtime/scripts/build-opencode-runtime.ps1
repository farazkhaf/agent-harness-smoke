param(
    [string]$RepoRoot = "",
    [string]$Image = "harness-smoke/opencode:1.18.30"
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
$dockerContext = Join-Path $RepoRoot "runtime\images\opencode"

Write-Host "Building $Image from $dockerContext"
docker build --progress=plain -t $Image $dockerContext
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Runtime image built. Verifying installed agent..."
docker run --rm $Image bash -lc '. "$HOME/.nvm/nvm.sh"; command -v node; command -v npm; command -v opencode; node --version; npm --version; opencode --version; command -v stdbuf'
exit $LASTEXITCODE
