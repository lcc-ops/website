# run_daily_batch.ps1 — orchestrator. Sequences the daily auto-draft pipeline.
#
# Phase order:
#   1. flock + init log + state.json rollback-on-corruption
#   2. _run_crawl.ps1       (zsxq then x; each cdp.py spawns Chrome if needed)
#   3. _build_prompts.py    (queue per-candidate prompt JSON)
#   4. _draft_one.ps1 x N   (sequential, one claude.cmd -p per slug)
#   5. _anti_ai_check.py    (move contaminated out of blog/)
#   6. _build_and_summarize.ps1 (pnpm build, roll back on fail, write state.json)
#
# Argument: --autonomous  (called from schtasks; log to file only)
# Exit: 0 = end-to-end ok. 1 = some phase failed.

[CmdletBinding()]
param(
    [switch]$Autonomous
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$RepoRoot       = (Resolve-Path "$PSScriptRoot\..\..").Path
$LogDir         = Join-Path $RepoRoot "scripts\auto\logs"
$LogPath        = Join-Path $LogDir ("$((Get-Date -Format 'yyyy-MM-dd')).log")
$QueueDir       = Join-Path $RepoRoot "scripts\auto\_queue"
$StatePath      = Join-Path $RepoRoot "scripts\auto\state.json"
$LockPath       = Join-Path $RepoRoot "scripts\auto\state.lock"
$BlogRoot       = Join-Path $RepoRoot "src\content\blog"

New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path $QueueDir -Force | Out-Null

function Write-Log {
    param([string]$Msg, [string]$Level = "INFO")
    $line = "[{0}] {1} {2}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ss"), $Level, $Msg
    if (-not $Autonomous) { Write-Host $line }
    Add-Content -Path $LogPath -Value $line -Encoding UTF8
}

# Phase 0: flock — PID-based; auto-clears if the holding process is dead.
if (Test-Path $LockPath) {
    $holder = (Get-Content -Raw -Path $LockPath -ErrorAction SilentlyContinue).Trim()
    $alive = $false
    if ($holder -match '^\d+$') {
        $alive = (Get-Process -Id ([int]$holder) -ErrorAction SilentlyContinue) -ne $null
    }
    if ($alive) {
        Write-Log "another batch is running (pid=$holder alive); exiting 0" "WARN"
        exit 0
    } else {
        Write-Log "stale lock (holder '$holder' not alive); removing" "WARN"
        Remove-Item $LockPath -Force -ErrorAction SilentlyContinue
    }
}
Set-Content -Path $LockPath -Value "$PID" -Force -Encoding UTF8
try {

    Write-Log "batch start (autonomous=$Autonomous)"
    Write-Log "RepoRoot=$RepoRoot"

    # State.json rollback-on-corruption
    if (Test-Path $StatePath) {
        try {
            $stateProbe = Get-Content -Raw -Path $StatePath | ConvertFrom-Json
            Write-Log "state.json ok"
        } catch {
            $bak = "$StatePath.bak.$((Get-Date -Format 'yyyy-MM-dd-HHmmss'))"
            Move-Item -Path $StatePath -Destination $bak -Force
            Write-Log "corrupt state.json moved to $bak; will re-init" "WARN"
        }
    } else {
        $init = [pscustomobject]@{
            last_run_date=$null; last_run_exit=$null; last_slugs=@()
            draft_status=@{}; last_build_exit=$null; history=@()
            last_successful_run_at=$null
        }
        $init | ConvertTo-Json -Depth 5 | Set-Content -Path $StatePath -Encoding UTF8
        Write-Log "state.json created"
    }

    # Phase 1: crawl (each cdp.py spawns Chrome if its CDP port is down)
    Write-Log "--- phase 1: crawl ---"
    & (Join-Path $PSScriptRoot "_run_crawl.ps1") -Autonomous:$Autonomous -LogPath $LogPath
    $phase1 = $LASTEXITCODE
    if ($phase1 -ne 0) {
        Write-Log "crawl returned non-zero (will continue anyway)" "WARN"
    }

    # Phase 2: build prompt queue
    Write-Log "--- phase 2: build_prompts ---"
    $queueOut = & python scripts/auto/_build_prompts.py --since-hours 24 --top 5 --threshold 6 2>&1
    $queueExit = $LASTEXITCODE
    Add-Content -Path $LogPath -Value ($queueOut -join "`n") -Encoding UTF8
    if ($queueExit -ne 0) {
        Write-Log "build_prompts failed; aborting batch" "ERROR"
        exit 1
    }
    # If queue empty, _draft_one phase becomes a no-op.
    $queueFiles = @(Get-ChildItem -Path $QueueDir -Filter "*.json" -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne "_summary.json" })
    Write-Log ("queue size = " + $queueFiles.Count)

    if ($queueFiles.Count -eq 0) {
        Write-Log "no candidates; batch exits 0 with no drafts"
        $today = Get-Date -Format "yyyy-MM-dd"
        $statusMap = @{}
        if (Test-Path $StatePath) {
            try {
                $st = Get-Content -Raw -Path $StatePath | ConvertFrom-Json
            } catch { $st = $null }
        }
        # best-effort state write
        $stObj = [pscustomobject]@{
            last_run_date            = $today
            last_run_exit            = 0
            last_slugs               = @()
            draft_status             = $statusMap
            last_build_exit          = 0
            last_successful_run_at   = $null
        }
        $stObj | ConvertTo-Json -Depth 5 | Set-Content -Path $StatePath -Encoding UTF8
        exit 0
    }

    # Phase 3: draft each
    Write-Log "--- phase 3: draft_one (x$($queueFiles.Count)) ---"
    $consecutiveTimeouts = 0
    $draftedSlugs = @()
    foreach ($qf in $queueFiles) {
        $qfPath = $qf.FullName
        Write-Log ("drafting " + $qf.Name)
        & (Join-Path $PSScriptRoot "_draft_one.ps1") -QueueFile $qfPath -Autonomous:$Autonomous -LogPath $LogPath
        $code = $LASTEXITCODE
        if ($code -eq 2) {
            $consecutiveTimeouts++
            Write-Log "consecutive timeouts = $consecutiveTimeouts" "WARN"
            if ($consecutiveTimeouts -ge 2) {
                Write-Log "two consecutive timeouts; aborting batch" "ERROR"
                exit 1
            }
        } else {
            $consecutiveTimeouts = 0
        }
        if ($code -eq 0) {
            try {
                $payload = Get-Content -Raw -Path $qfPath | ConvertFrom-Json
                $draftedSlugs += $payload.slug
            } catch {}
        }
    }
    Write-Log ("drafted slugs: " + ($draftedSlugs -join ","))

    # Phase 4: anti-AI check + pnpm build
    Write-Log "--- phase 4: anti-AI + build ---"
    & (Join-Path $PSScriptRoot "_build_and_summarize.ps1") -Autonomous:$Autonomous -LogPath $LogPath
    $phase4 = $LASTEXITCODE

    if ($phase4 -ne 0) {
        Write-Log "build_and_summarize failed" "ERROR"
        exit 1
    }
    Write-Log "batch end OK"
    exit 0
} finally {
    Remove-Item -Path $LockPath -Force -ErrorAction SilentlyContinue
}
