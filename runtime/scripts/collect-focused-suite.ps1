param(
    [string]$RepoRoot = "",
    [string]$SuitePath = "suites\batchline-focused\suite.toml",
    [Parameter(Mandatory = $true)][string]$ReportsRoot,
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
if (-not [System.IO.Path]::IsPathRooted($SuitePath)) { $SuitePath = Join-Path $RepoRoot $SuitePath }
if (-not [System.IO.Path]::IsPathRooted($ReportsRoot)) { $ReportsRoot = Join-Path $RepoRoot $ReportsRoot }
if (-not $OutputPath) { $OutputPath = $ReportsRoot }
elseif (-not [System.IO.Path]::IsPathRooted($OutputPath)) { $OutputPath = Join-Path $RepoRoot $OutputPath }

python (Join-Path $RepoRoot "runtime\suite\collect_suite.py") `
    --suite $SuitePath `
    --reports-root $ReportsRoot `
    --out $OutputPath
exit $LASTEXITCODE
