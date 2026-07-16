# _run_crawl.ps1 — invoke both crawlers. NO retry on scrape failure.
#
# Each crawler (scrapers/crawl.py, scrapers_x/crawl.py) launches its own
# headless Chrome via Playwright and closes it on context exit — nothing
# to clean up here.
#
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File _run_crawl.ps1
# Exit:  always 0 (crawl failures are logged, not raised; per user policy).

[CmdletBinding()]
param(
    [string]$RepoRoot = "D:\LocalSystem\Code\ai_dev\website",
    [string]$LogPath = "",
    [switch]$Autonomous
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

Set-Location $RepoRoot

function Write-Log {
    param([string]$Msg)
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ss"), $Msg
    if (-not $Autonomous) { Write-Host $line }
    if ($LogPath -ne "") { Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
}

$results = @()

Write-Log "zsxq crawl starting"
$zsxqOut = & python scripts/scrapers/crawl.py --mode auto --cdp http://localhost:9225 --count 30 --humane-delay-ms 3000 6000 2>&1
$zsxqExit = $LASTEXITCODE
if ($LogPath -ne "") {
    Add-Content -Path $LogPath -Value ($zsxqOut -join "`n") -Encoding UTF8
} elseif (-not $Autonomous) {
    $zsxqOut | ForEach-Object { Write-Host $_ }
}
$results += @{ name = "zsxq"; exit = $zsxqExit }

Start-Sleep -Seconds 2

Write-Log "x.com crawl starting"
$xOut = & python scripts/scrapers_x/crawl.py --mode auto --scroll-rounds 3 --humane-delay-ms 3000 6000 2>&1
$xExit = $LASTEXITCODE
if ($LogPath -ne "") {
    Add-Content -Path $LogPath -Value ($xOut -join "`n") -Encoding UTF8
} elseif (-not $Autonomous) {
    $xOut | ForEach-Object { Write-Host $_ }
}
$results += @{ name = "x"; exit = $xExit }

Write-Log ("crawl summary: " + (($results | ForEach-Object { "$($_.name)=exit$($_.exit)" }) -join ", "))
exit 0
