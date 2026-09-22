param(
    [string]$RepoRoot = "",
    [Parameter(Mandatory = $true)][string]$SuitePath,
    [string]$TrialsRoot = "",
    [string]$OutputRoot = "",
    [string[]]$TaskId = @(),
    [string[]]$ProfileId = @(),
    [switch]$PlanOnly,
    [switch]$KeepResolvedTask,
    [switch]$ContinueOnFailure
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

if (-not [System.IO.Path]::IsPathRooted($SuitePath)) {
    $SuitePath = Join-Path $RepoRoot $SuitePath
}

$runtimeRoot = Join-Path $RepoRoot "runtime"
$suiteJson = python (Join-Path $runtimeRoot "suite\suite_config.py") $SuitePath
if ($LASTEXITCODE -ne 0) { throw "Failed to load suite metadata." }
$suiteMeta = $suiteJson | ConvertFrom-Json

if (-not $OutputRoot) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    if ($suiteMeta.kind -eq "scenario") {
        $safeSuiteId = ($suiteMeta.id -replace '[^A-Za-z0-9._-]', '_')
        $OutputRoot = Join-Path $RepoRoot ("results\batchline-scenarios\{0}\{1}" -f $safeSuiteId, $stamp)
    } else {
        $OutputRoot = Join-Path $RepoRoot ("results\batchline-focused\{0}" -f $stamp)
    }
} elseif (-not [System.IO.Path]::IsPathRooted($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot $OutputRoot
}

if (-not $TrialsRoot) {
    $TrialsRoot = Join-Path $RepoRoot "trials"
} elseif (-not [System.IO.Path]::IsPathRooted($TrialsRoot)) {
    $TrialsRoot = Join-Path $RepoRoot $TrialsRoot
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
New-Item -ItemType Directory -Force -Path $TrialsRoot | Out-Null
$planJson = python (Join-Path $runtimeRoot "suite\suite_config.py") $SuitePath --plan
if ($LASTEXITCODE -ne 0) { throw "Failed to load suite plan." }
$parsedPlan = $planJson | ConvertFrom-Json
$plan = @()
foreach ($item in $parsedPlan) { $plan += $item }
if ($TaskId.Count -gt 0) { $plan = @($plan | Where-Object { $TaskId -contains $_.task_id }) }
if ($ProfileId.Count -gt 0) { $plan = @($plan | Where-Object { $ProfileId -contains $_.profile_id }) }
if ($plan.Count -eq 0) { throw "Suite filters selected no runs." }

if ($PlanOnly) {
    $plan | Select-Object task_id, profile_id, execution, attempt, model | Format-Table -AutoSize
    exit 0
}

function Get-TrialResultPaths {
    if (-not (Test-Path $TrialsRoot)) { return @() }
    return @(
        Get-ChildItem -Path $TrialsRoot -Recurse -Filter result.json -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "[\\/]smoke-report[\\/]" } |
        ForEach-Object {
            try {
                $data = Get-Content -Raw $_.FullName | ConvertFrom-Json
                if ($null -ne $data.agent_result -and $null -ne $data.verifier_result) { $_.FullName }
            } catch {
                # Ignore incomplete/non-trial result files while Harbor is writing elsewhere.
            }
        }
    )
}

$runIndex = 0
foreach ($entry in $plan) {
    $runIndex += 1
    Write-Host ""
    Write-Host ("[{0}/{1}] {2} :: {3} :: attempt {4}" -f $runIndex, $plan.Count, $entry.task_id, $entry.profile_id, $entry.attempt)

    $before = @{}
    foreach ($p in (Get-TrialResultPaths)) { $before[$p] = $true }

    if ($entry.execution -eq "preinstalled") {
        & (Join-Path $runtimeRoot "scripts\run-preinstalled.ps1") `
            -RepoRoot $RepoRoot `
            -TaskPath $entry.task_path `
            -RuntimeProfile $entry.runtime_profile `
            -Model $entry.model `
            -TrialsRoot $TrialsRoot `
            -KeepResolvedTask:$KeepResolvedTask
        $runExit = $LASTEXITCODE
    } elseif ($entry.execution -eq "external") {
        $externalArgs = @{
            RepoRoot = $RepoRoot
            TaskPath = $entry.task_path
            Agent = $entry.agent
            TrialsRoot = $TrialsRoot
        }
        if ($entry.model) { $externalArgs["Model"] = $entry.model }
        & (Join-Path $runtimeRoot "scripts\run-external.ps1") @externalArgs
        $runExit = $LASTEXITCODE
    } else {
        throw "Unsupported suite execution mode: $($entry.execution)"
    }

    $newResults = @(
        Get-TrialResultPaths |
        Where-Object { -not $before.ContainsKey($_) } |
        Sort-Object { (Get-Item $_).LastWriteTimeUtc } -Descending
    )

    if ($newResults.Count -eq 0) {
        $message = "Harbor run completed but no new trial result.json was found under $TrialsRoot. Pass the correct -TrialsRoot."
        if ($ContinueOnFailure) { Write-Warning $message } else { throw $message }
    } else {
        $trialResult = $newResults[0]
        $trialDir = Split-Path $trialResult -Parent
        $safeTask = ($entry.task_id -replace '[^A-Za-z0-9._-]', '_')
        $runOut = Join-Path $OutputRoot ("runs\{0}\{1}\attempt-{2}" -f $safeTask, $entry.profile_id, $entry.attempt)
        New-Item -ItemType Directory -Force -Path $runOut | Out-Null
        python (Join-Path $runtimeRoot "report\report_trial.py") $trialDir --out $runOut
        if ($LASTEXITCODE -ne 0) {
            if ($ContinueOnFailure) { Write-Warning "Report normalization failed for $trialDir" } else { throw "Report normalization failed for $trialDir" }
        }
    }

    if ($runExit -ne 0 -and -not $ContinueOnFailure) {
        throw "Harbor run failed with exit code $runExit"
    }
}

python (Join-Path $runtimeRoot "suite\collect_suite.py") `
    --suite $SuitePath `
    --reports-root $OutputRoot `
    --out $OutputRoot
if ($LASTEXITCODE -ne 0) { throw "Suite collection failed." }

Write-Host "Suite results: $OutputRoot"
