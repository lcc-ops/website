# scripts/auto — Autonomous Daily Blog Draft Batch

End-to-end automated pipeline: pull fresh posts from zsxq + x.com, draft one
bilingual case-study blog per top candidate via headless Claude, run pnpm build,
clean up contaminated drafts.

**Triggered by Windows Task Scheduler at 09:00 daily.** Manual / one-shot run:

```powershell
cd D:\LocalSystem\Code\ai_dev\website
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\auto\run_daily_batch.ps1 -Autonomous
```

Inspect after a run:

```powershell
Get-Content .\scripts\auto\logs\<today>.log
Get-Content .\scripts\auto\state.json
Get-ChildItem .\src\content\blog\      # today's new slugs
Get-ChildItem .\scripts\auto\_archive\ # contaminated / failed drafts
```

## What it does (in order)

1. **flock** — if `state.lock` < 60 min old, exits 0 (concurrent runs).
2. **preflight** — checks Chrome DevTools at `:9225` (zsxq) and `:9228` (x.com);
   if a port is down, retries 3× with 1.5/3/5 s backoff and finally spawns the
   missing Chrome instance with the matching user-data-dir under
   `D:\LocalSystem\Code\ai_dev\multi_publisher\profiles\profile-<port>\`.
3. **crawl** — runs the existing `scripts/scrapers/crawl.py` then
   `scripts/scrapers_x/crawl.py`. No retry on scrape failure.
4. **build_prompts** — `scripts/auto/_build_prompts.py` reads both SQLite DBs,
   applies the AI-keyword + score ≥ 6 + top 5 filter, dedups vs
   `state.json.last_slugs`, and writes per-candidate prompt JSON into
   `scripts/auto/_queue/`.
5. **draft_one (× N)** — sequentially invokes `claude.cmd -p "<prompt>"`,
   parses `=== en.md ===` / `=== zh.md ===` blocks, writes both `.md` files
   into `src\content\blog\<slug>\`. Single 30-min timeout per call.
   Two consecutive timeouts aborts the batch.
6. **anti_ai_check** — `scripts/auto/_anti_ai_check.py` greps each new `.md`
   against `weights.json` + banned-phrase regex list. Thresholds:
   `en weighted ≥ 4` or `zh weighted ≥ 6` ⇒ contaminated; any banned phrase ⇒
   contaminated; missing pair (en xor zh) ⇒ contaminated. Contaminated drafts
   are moved to `scripts/auto\_archive\<today>\<slug>\`.
7. **build_and_summarize** — runs `pnpm build`. On exit 0, marks every kept
   slug `kept` in `state.json`, logs `DONE: <n> drafts`. On exit ≠ 0, removes
   every kept-slug folder, marks them `discarded`, exits 1.

Failure contract: any phase aborts with exit 1 → log line + exit code stays
visible in `schtasks` "Last Result" and in `state.json.last_run_exit`.
Contaminated drafts never enter `src/content/blog/`. Failed drafts (Claude
timeout / parse error) live only in `scripts/auto\_archive\<today>\` if the
queue JSON was saved before the failure.

## State

`scripts/auto/state.json` schema:

```json
{
  "last_run_date": "2026-07-13",
  "last_run_exit": 0,
  "last_slugs": ["...", "..."],
  "draft_status": { "<slug>": "kept" | "contaminated" | "discarded" },
  "last_build_exit": 0,
  "history": [],
  "last_successful_run_at": "2026-07-15T09:00:00Z"
}
```

- `last_successful_run_at` — ISO-8601 UTC `Z`-suffixed timestamp of the last
  build that exited 0. Stays `null` until the first successful build. Read by
  `_alert_stale_run.ps1`; see "Stale-run detection" below.
- `history` — appended on every successful end-to-end run; each entry is
  `{ run_at, slugs, exit, build_exit }`. List is FIFO-trimmed to the last
  64 entries inside `_build_and_summarize.ps1`'s `Update-State` helper.

`scripts/auto/state.lock` blocks a second batch from running within 60 min of
the prior. Stale locks (>60 min) are removed at start.

Logs: `scripts/auto/logs/YYYY-MM-DD.log`. 90-day retention enforced at the
start of every build.

## Stale-run detection

Cookie expiry, schtasks being disabled, and a CDP launch failure all share
the same observable symptom: `state.json.last_run_date` either does not
advance to today's date, or the batch exits 0 with `last_slugs = []`.
`_alert_stale_run.ps1` exists to catch the *successful* failure mode, where
the batch says "OK" but no end-to-end build has succeeded in `StaleHours`.

```powershell
# Returns 0 if last_successful_run_at is null or within StaleHours,
# 1 if older than StaleHours (default 36 h),
# 2 if state.json is missing or unparseable.
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\auto\_alert_stale_run.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\auto\_alert_stale_run.ps1 -StaleHours 48
```

Hook it to whatever downstream sink you already use (a webhook, a sheet,
`Send-MailMessage`, an `Enter` notification). The exit code is the contract
— do not parse the Write-Host body.

### Register the schtasks alarm

```bat
:: Run from a non-elevated cmd, same user-context as AutoDailyBlogDraft.
scripts\check\step7b__register_alert_schtasks.bat
```

Then verify:

```powershell
schtasks /query /tn AutoAlertStaleRun /v /fo LIST
schtasks /run /tn AutoAlertStaleRun           # force a manual trigger now
```

### Uninstall

```bat
schtasks /delete /tn "AutoAlertStaleRun" /f
```

Picking 11:00 (≠ 09:00 batch, with a 60-second /delay for desktop wake)
keeps alert checks from racing the batch and gives the batch two hours of
headroom before tripping the 36 h threshold.

## Anti-AI defence

1. The headless prompt (`scripts/auto/_prompts/draft_one_topic.md`) lists 50+
   English banned words and 30+ Chinese banned words plus 12 banned phrases /
   patterns, and demands a self-check before printing.
2. The post-draft check (`scripts/auto/_anti_ai_check.py`) re-scans every
   emitted `.md` against the same weighted word list + banned phrase regex.
   Contaminated drafts are *moved out of `src/content/blog/`* so they never
   reach `pnpm build`.

The setup is best-effort. Final proofreading is **lost** in autonomous mode —
that is the user's call and is documented in the project memory.

## NOT in scope

- No git commit / push. **Never.** Verified by your project's `git-workflow.md`
  rules. The batch only writes draft files; the user inspects and commits
  themselves.
- No external notifications (email / Slack / Telegram). Status is in
  `state.json` and Task Scheduler "Last Result".
- No cookie-refresh. If zsxq or x.com cookies expire, both crawls return
  empty and the batch exits 0 cleanly with `last_slugs = []`. Re-login
  manually in the matching Chrome profile, then trigger another run.

## Manual run once

```powershell
cd D:\LocalSystem\Code\ai_dev\website
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\auto\run_daily_batch.ps1 -Autonomous
```

Without `-Autonomous`, the script also streams its progress to the host
console (handy for the first few smoke-tests).

## Register

```bat
:: One-shot, user-account context. Run from a non-elevated cmd.
scripts\check\step7a__register_schtasks.bat
```

Then verify:

```powershell
Get-ScheduledTask -TaskName AutoDailyBlogDraft | Format-List
schtasks /run /tn AutoDailyBlogDraft      # force a manual trigger now
```

## Uninstall

```bat
schtasks /delete /tn "AutoDailyBlogDraft" /f
```

The `scripts/auto/` directory itself can stay; nothing else touches it.
