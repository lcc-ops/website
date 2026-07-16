# _draft_one.ps1 — invoke `claude.cmd -p` for one queue entry and split its
# output into src/content/blog/<slug>/{en,zh}.md.
#
# The prompt is delivered via stdin (not -ArgumentList) to dodge the
# Windows 32K cmdline limit. The child is invoked as the underlying
# claude.exe (not the .cmd shim) so .NET's UTF-8 StreamReader can read
# stdout without the PowerShell host's ANSI codepage mangling non-ASCII.
#
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File _draft_one.ps1 `
#                       -QueueFile scripts/auto/_queue/<file>.json
# Exit: 0 = wrote both files. 1 = Claude call failed or frontmatter missing.
#       2 = claude.exe timed out (consumer escalates to batch abort).

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$QueueFile,
    [string]$RepoRoot = "D:\LocalSystem\Code\ai_dev\website",
    [string]$LogPath = "",
    [switch]$Autonomous,
    [int]$TimeoutSec = 1800
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Resolve the underlying claude.exe so we can attach stdin directly.
# claude.cmd is a thin @echo-off + %* passthrough — calling the .exe
# avoids an extra cmd.exe hop and makes UTF-8 stdin/stdout reliable.
$claudeCmd   = "D:\LocalSystem\envs\nodeJs\node_24\node_global\claude.cmd"
$claudeExe   = "D:\LocalSystem\envs\nodeJs\node_24\node_global\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
if (-not (Test-Path $claudeExe)) {
    # Fall back to the .cmd shim if the .exe path is wrong (env change
    # by the user). The .cmd shim is more portable across env layouts.
    if (Test-Path $claudeCmd) {
        $claudeExe = $claudeCmd
    } else {
        Write-Log "claude not found at $claudeExe or $claudeCmd" "ERROR"
        exit 1
    }
}

function Write-Log {
    param([string]$Msg, [string]$Level = "INFO")
    $line = "[{0}] {1} {2}" -f (Get-Date -Format "yyyy-MM-ddTHH:mm:ss"), $Level, $Msg
    if (-not $Autonomous) { Write-Host $line }
    if ($LogPath -ne "") { Add-Content -Path $LogPath -Value $line -Encoding UTF8 }
}

if (-not (Test-Path $QueueFile)) {
    Write-Log "queue file missing: $QueueFile" "ERROR"
    exit 1
}

# Read queue JSON as raw bytes + UTF-8 decode. Get-Content on a cp936
# PowerShell host re-encodes non-ASCII codepoints to '?' and breaks
# ConvertFrom-Json (ArgumentException). The queue files are written by
# Python with ensure_ascii=False, so they are valid UTF-8.
$jsonBytes = [System.IO.File]::ReadAllBytes($QueueFile)
$jsonText  = [System.Text.Encoding]::UTF8.GetString($jsonBytes)
$payload   = $jsonText | ConvertFrom-Json
$slug      = $payload.slug
$source    = $payload.source_table
$rowId     = $payload.row_id

Write-Log "drafting $slug (source=$source row=$rowId)"

$prompt = $payload.prompt
$destDir = Join-Path $RepoRoot "src\content\blog\$slug"

$env:CLAUDE_TIMEOUT_MS = [string]($TimeoutSec * 1000)
$env:NO_COLOR = "1"

# Build the process with stdin/stdout/stderr redirected as raw byte streams.
# We pass the prompt via stdin (no argv-length cap) and read stdout as raw
# bytes (so PowerShell's ANSI codepage can't mangle non-ASCII text).
$proc = New-Object System.Diagnostics.Process
$proc.StartInfo.FileName = $claudeExe
$proc.StartInfo.Arguments = "-p --output-format text"
$proc.StartInfo.UseShellExecute = $false
$proc.StartInfo.RedirectStandardInput  = $true
$proc.StartInfo.RedirectStandardOutput = $true
$proc.StartInfo.RedirectStandardError  = $true
$proc.StartInfo.CreateNoWindow = $true

$started = $false
try {
    [void]$proc.Start()
    $started = $true

    # Write prompt to stdin as UTF-8 (no BOM). We flush and dispose the
    # writer (which closes the underlying pipe write end) but do NOT call
    # $proc.StandardInput.Close() — calling Close on the Process's
    # StandardInput directly on PowerShell 5.1 + claude.exe has been
    # observed to keep HasExited false even after the child has produced
    # all its output. Disposing the StreamWriter is sufficient to send
    # EOF to the child.
    $stdinWriter = [System.IO.StreamWriter]::new(
        $proc.StandardInput.BaseStream,
        [System.Text.UTF8Encoding]::new($false)
    )
    $stdinWriter.Write($prompt)
    $stdinWriter.Flush()
    $stdinWriter.Dispose()
    $stdinWriter = $null

    # Bounded wait for child exit. PowerShell 5.1's Process.WaitForExit(int)
    # is documented to return false even after the child has fully exited
    # when the parent still has unread data on stdout/stderr. Polling
    # HasExited on a 200ms cadence and then doing one final WaitForExit()
    # (no arg) is the documented workaround.
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while (-not $proc.HasExited -and (Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 200
    }
    if (-not $proc.HasExited) {
        try { $proc.Kill($true) } catch {}
        Write-Log "claude timed out after ${TimeoutSec}s for $slug" "ERROR"
        exit 2
    }
    # Final wait-for-exit with no timeout. By this point HasExited is true;
    # this call returns immediately and flushes any final state.
    [void]$proc.WaitForExit()

    # Now that the child has exited, its stdout/stderr BaseStreams are
    # closed and the bytes are fully drained. CopyTo reads from a closed
    # underlying pipe and never blocks; this dodges the PowerShell host's
    # ANSI codepage mangling of non-ASCII output that would happen if we
    # read via the TextReader (StandardOutput).
    $outMs = New-Object System.IO.MemoryStream
    $proc.StandardOutput.BaseStream.CopyTo($outMs)
    $outBytes = $outMs.ToArray()
    $errMs = New-Object System.IO.MemoryStream
    $proc.StandardError.BaseStream.CopyTo($errMs)
    $errBytes = $errMs.ToArray()
} finally {
    if ($started) {
        if ($stdinWriter) {
            try { $stdinWriter.Dispose() } catch {}
        }
        if (-not $proc.HasExited) {
            try { $proc.Kill($true) } catch {}
        }
    }
}

# claude.exe writes UTF-8 (verified empirically; the .exe does not emit a
# BOM and uses the same encoding it accepts on stdin).
$raw = [System.Text.Encoding]::UTF8.GetString($outBytes)
$err = [System.Text.Encoding]::UTF8.GetString($errBytes)
$exit = $proc.ExitCode

if ($exit -ne 0) {
    Write-Log "claude exit=$exit for $slug; err=$err" "ERROR"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($raw)) {
    Write-Log "claude returned empty output for $slug" "ERROR"
    exit 1
}

$enBlock = [regex]::Match($raw, '(?s)=== en\.md ===\s*\n(.*?)\n=== zh\.md ===')
$zhBlock = [regex]::Match($raw, '(?s)=== zh\.md ===\s*\n(.*?)\s*$')

if (-not $enBlock.Success -or -not $zhBlock.Success) {
    Write-Log "could not find en/zh code blocks in claude output for $slug" "ERROR"
    # Fall back: if the model wrote the files directly to disk (a behavior
    # the trial surfaced — claude occasionally does this when the prompt
    # contains "produce en.md and zh.md"), accept whatever ended up in the
    # destination directory and bail out cleanly.
    $enPath = Join-Path $destDir "en.md"
    $zhPath = Join-Path $destDir "zh.md"
    if ((Test-Path $enPath) -and (Test-Path $zhPath)) {
        Write-Log "claude wrote $slug\{en,zh}.md directly to disk; accepting" "WARN"
        exit 0
    }
    Add-Content -Path $LogPath -Value ("---raw---`n" + $raw + "`n---end---") -Encoding UTF8 -ErrorAction SilentlyContinue
    exit 1
}

$enContent = $enBlock.Groups[1].Value.TrimEnd() + "`n"
$zhContent = $zhBlock.Groups[1].Value.TrimEnd() + "`n"

if (-not $enContent.StartsWith("---")) {
    Write-Log "en.md does not start with frontmatter fence for $slug" "ERROR"
    exit 1
}
if (-not $zhContent.StartsWith("---")) {
    Write-Log "zh.md does not start with frontmatter fence for $slug" "ERROR"
    exit 1
}

New-Item -ItemType Directory -Path $destDir -Force | Out-Null
[System.IO.File]::WriteAllText((Join-Path $destDir "en.md"), $enContent, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $destDir "zh.md"), $zhContent, [System.Text.UTF8Encoding]::new($false))

Write-Log "wrote $slug\{en,zh}.md"
exit 0
