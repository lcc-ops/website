# _build_and_summarize.ps1 — run anti-AI check, then pnpm build, then write final state.
#
# On build fail: remove every kept-slug folder under src/content/blog that was
# created today (or matches draft_status=kept in state.json), mark them
# discarded, exit 1.
#
# On success: mark kept, log "DONE: <n> drafts", exit 0.

[CmdletBinding()]
param(
    [string]$RepoRoot = "D:\LocalSystem\Code\ai_dev\website",
    [string]$LogPath = "",
    [switch]$Autonomous
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

function Write-Log {
    param([string]$Msg, [string]$Level = "INFO")
    $line = "[{0}] {1} {2}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ss"), $Level, $Msg
    if (-not $Autonomous) { Write-Host $line }
    if ($LogPath -ne "") { Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
}

function Update-State {
    param([hashtable]$Changes)
    $statePath = Join-Path $RepoRoot "scripts\auto\state.json"
    if (Test-Path $statePath) {
        try { $state = Get-Content -Raw -Path $statePath | ConvertFrom-Json } catch {
            $state = [pscustomobject]@{
                last_run_date = $null; last_run_exit = $null; last_slugs = @()
                draft_status = @{}; last_build_exit = $null; history = @()
            }
        }
    } else {
        $state = [pscustomobject]@{
            last_run_date = $null; last_run_exit = $null; last_slugs = @()
            draft_status = @{}; last_build_exit = $null; history = @()
            last_successful_run_at = $null
        }
    }

    foreach ($k in $Changes.Keys) {
        $val = $Changes[$k]
        # Special handling for history_append: extend history[] and trim to 64.
        if ($k -eq "history_append" -and $null -ne $val) {
            $existing = @()
            if ($state.PSObject.Properties.Name -contains "history" -and $state.history) {
                $existing = @($state.history)
            }
            $existing += $val
            if ($existing.Count -gt 64) {
                $existing = @($existing | Select-Object -Last 64)
            }
            if ($state.PSObject.Properties.Name -contains "history") {
                $state.history = $existing
            } else {
                $state | Add-Member -NotePropertyName "history" -NotePropertyValue $existing
            }
            continue
        }
        if ($null -eq $state.$k) {
            $state | Add-Member -NotePropertyName $k -NotePropertyValue $val
        } else {
            $state.$k = $val
        }
    }
    $state | ConvertTo-Json -Depth 10 | Set-Content -Path $statePath -Encoding UTF8
}

Set-Location $RepoRoot
$today = Get-Date -Format "yyyy-MM-dd"

# Purge logs older than 90 days.
$logsDir = Join-Path $RepoRoot "scripts\auto\logs"
if (Test-Path $logsDir) {
    Get-ChildItem -Path $logsDir -File | Where-Object {
        ($_.LastWriteTime -lt (Get-Date).AddDays(-90))
    } | ForEach-Object {
        Write-Log "purging log $($_.Name)"
        Remove-Item $_.FullName -Force
    }
}

# Step A: anti-AI check
Write-Log "running anti-AI check"
$antiOut = & python scripts/auto/_anti_ai_check.py --today $today 2>&1
$antiExit = $LASTEXITCODE
if ($LogPath -ne "") { Add-Content -Path $LogPath -Value ($antiOut -join "`n") -Encoding UTF8 }

# Parse last JSON object emitted on stdout.
$reportObj = $null
$lines = @()
$antiOut | ForEach-Object { $lines += $_ }
$jsonText = ($lines | Where-Object { $_.Trim().StartsWith("{") -and $_.Trim().EndsWith("}") }) -join "`n"
if ($jsonText) {
    try { $reportObj = $jsonText | ConvertFrom-Json } catch {}
}
if ($reportObj) {
    Write-Log ("anti-AI: clean=" + $reportObj.clean.Count + " contaminated=" + $reportObj.contaminated.Count)
} else {
    Write-Log "anti-AI check did not produce a JSON report; proceeding anyway" "WARN"
}

# Build kept-slug list from JSON report (clean slugs that survived anti-AI check).
$keptSlugs = @()
if ($reportObj -and $reportObj.clean) {
    foreach ($c in $reportObj.clean) { $keptSlugs += $c.slug }
}

# Step B: pnpm build
Write-Log "running pnpm build"
$env:CI = "1"
$env:NODE_ENV = "production"

$buildOut = & pnpm build 2>&1
$buildExit = $LASTEXITCODE
if ($LogPath -ne "") {
    Add-Content -Path $LogPath -Value ($buildOut -join "`n") -Encoding UTF8
} elseif (-not $Autonomous) {
    $buildOut | ForEach-Object { Write-Host $_ }
}

if ($buildExit -eq 0) {
    Write-Log ("BUILD OK. kept=" + ($keptSlugs -join ","))
    $statusMap = @{}
    foreach ($s in $keptSlugs) { $statusMap[$s] = "kept" }
    # Stamp end-to-end success and append a history entry. Update-State
    # accepts arbitrary keys and writes via foreach → the two new fields
    # are pure additive. _alert_stale_run.ps1 reads last_successful_run_at
    # to detect silent failures (cookie expiry, schtasks disabled, etc.).
    $okAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Update-State @{
        last_run_date            = $today
        last_run_exit            = 0
        last_slugs               = $keptSlugs
        draft_status             = $statusMap
        last_build_exit          = 0
        last_successful_run_at   = $okAt
        history_append           = [pscustomobject]@{
            run_at    = $okAt
            slugs     = $keptSlugs
            exit      = 0
            build_exit = 0
        }
    }
    Write-Log ("DONE: " + $keptSlugs.Count + " drafts kept")
    exit 0
}

Write-Log "BUILD FAILED; removing today's kept slugs" "ERROR"
$blogRoot = Join-Path $RepoRoot "src\content\blog"
foreach ($s in $keptSlugs) {
    $dir = Join-Path $blogRoot $s
    if (Test-Path $dir) {
        Write-Log ("rm -rf " + $dir)
        Remove-Item -Recurse -Force $dir -ErrorAction SilentlyContinue
    }
}
$statusMap = @{}
foreach ($s in $keptSlugs) { $statusMap[$s] = "discarded" }
Update-State @{
    last_run_date    = $today
    last_run_exit    = 1
    last_slugs       = $keptSlugs
    draft_status     = $statusMap
    last_build_exit  = $buildExit
}
exit 1
