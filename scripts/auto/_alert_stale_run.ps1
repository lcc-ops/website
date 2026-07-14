# _alert_stale_run.ps1 — silent-failure detector for the daily auto-batch.
#
# Reads state.json.last_successful_run_at (ISO-8601 UTC 'Z' suffix) and
# compares it to wall-clock time. Returns:
#   0 — fresh (within StaleHours), or never-run (null)
#   1 — stale: last_successful_run_at older than StaleHours
#   2 — state.json missing or unreadable
#
# Designed to be called from Task Scheduler (once per day, off-peak) or
# manually:
#   powershell -NoProfile -ExecutionPolicy Bypass -File _alert_stale_run.ps1
#   powershell -NoProfile -File _alert_stale_run.ps1 -StaleHours 48
#
# Exit code is the contract — hook it to whatever downstream consumer you
# have (curl a webhook, send-mailmessage, push state to a sheet). Do not use
# the body of Write-Host for parsing; pipe `$LASTEXITCODE` instead.

[CmdletBinding()]
param(
    [int]$StaleHours = 36,
    [string]$RepoRoot = "D:\LocalSystem\Code\ai_dev\website",
    [string]$LogPath = ""
)

$ErrorActionPreference = "Continue"

function Write-AlertLog {
    param([string]$Msg, [string]$Level = "INFO")
    $line = "[{0}] {1} {2}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"), $Level, $Msg
    Write-Host $line
    if ($LogPath -ne "") { Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
}

$statePath = Join-Path $RepoRoot "scripts\auto\state.json"
if (-not (Test-Path $statePath)) {
    Write-AlertLog "state.json missing at $statePath" "WARN"
    exit 2
}

try {
    $state = Get-Content -Raw -Path $statePath | ConvertFrom-Json
} catch {
    Write-AlertLog "state.json unparseable: $_" "WARN"
    exit 2
}

# last_successful_run_at is null on a fresh repo / never-finished batch.
$stamp = $state.last_successful_run_at
if ([string]::IsNullOrWhiteSpace($stamp)) {
    Write-AlertLog "last_successful_run_at is null; treating as fresh (no completed run yet)"
    exit 0
}

try {
    $last = [datetime]::Parse($stamp).ToUniversalTime()
} catch {
    Write-AlertLog "last_successful_run_at not parseable: '$stamp'" "WARN"
    exit 2
}

$now = (Get-Date).ToUniversalTime()
$ageHours = ($now - $last).TotalHours

if ($ageHours -gt $StaleHours) {
    Write-AlertLog ("STALE-RUN DETECTED: last success {0:N1}h ago (threshold {1}h)" -f $ageHours, $StaleHours) "WARN"
    exit 1
}

Write-AlertLog ("fresh: last success {0:N1}h ago (threshold {1}h)" -f $ageHours, $StaleHours)
exit 0
