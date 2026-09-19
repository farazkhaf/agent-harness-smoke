param(
    [Parameter(Mandatory = $true)]
    [string]$TrialPath,
    [string]$OutPath = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RuntimeRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Reporter = Join-Path $RuntimeRoot "report\report_trial.py"

if (-not (Test-Path $Reporter)) {
    throw "Reporter not found: $Reporter"
}

$argsList = @($Reporter, $TrialPath)
if ($OutPath) {
    $argsList += @("--out", $OutPath)
}

python @argsList
