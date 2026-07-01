---
name: twitter-x-daily-blog
version: 1.0.0
description: "Pull the latest AI-monetization posts from X/Twitter (logged in via Chrome on :9228), filter to AI-keyword cases, rank by engagement, and write bilingual drafts to src/content/blog/<slug>/{en,zh}.md for human review. Use when the user says 'pull today's X/Twitter AI-monetization posts and write them up', 'do the daily x.com pass', or invokes @twitter-x-daily-blog. Cold-eyed case-study tone, math-driven. Posts do NOT contain source attribution; provenance is internal."
metadata:
  repo_relative_paths:
    crawl_script: "scripts/scrapers_x/crawl.py"
    sqlite_path: "scripts/scrapers_x/data/x.sqlite3"
    output_root: "src/content/blog"
    existing_examples:
      - "src/content/blog/seedance-2-product-video-case"
      - "src/content/blog/kdp-ai-ebook-case"
      - "src/content/blog/vertical-ai-tools-gap"
      - "src/content/blog/etsy-ai-digital-products"
      - "src/content/blog/english-ai-seo-content-site"
---

# twitter-x-daily-blog

This skill turns a fresh pull of x.com AI-monetization posts into bilingual blog drafts for the project's AI Lab section.

It mirrors `zsxq-daily-blog` but reads from x.com search results instead of a knowledge-planet API. It uses the user's Chrome on CDP port :9228 (a separate Chrome instance from the :9225 one used for zsxq), scrapes the search results for AI-monetization tweets, deduplicates against a local SQLite, and drafts bilingual case studies.

## When to invoke

Trigger on any of:
- "pull today's X/Twitter AI-monetization posts and write them up"
- "do the daily x.com pass"
- "refresh x.com for new AI cases"
- "check x.com for new posts worth writing about"
- the user explicitly invokes `@twitter-x-daily-blog`

Do NOT invoke for:
- ad-hoc single-topic writing (use the regular conversational flow instead)
- reading or summarizing an existing blog post
- editing or reviewing an existing draft

## Pre-flight (run these checks first)

If any pre-flight check fails, abort with a one-sentence remediation.

1. CDP reachable. Run:
   ```bash
   curl -sf http://localhost:9228/json/version > /dev/null || abort "Chrome is not debugging on :9228 — relaunch with --remote-debugging-port=9228"
   ```
2. Scraper module importable. Run:
   ```bash
   python -c "import sys; sys.path.insert(0, 'scripts/scrapers_x'); from _lib import db, cdp, selectors" || abort "scraper module not importable — re-read scripts/scrapers_x/_lib"
   ```
3. SQLite present. Verify `scripts/scrapers_x/data/x.sqlite3` exists. If not, run a full crawl once before doing incremental.

## Working procedure

The skill is a recipe for **you (Claude)** to execute. The skill does NOT spawn sub-servers, run any scheduled task, or call external APIs. All the work is done by you reading, evaluating, writing files.

### Step 1: Run the crawl

```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode auto --scroll-rounds 5 --humane-delay-ms 800 1400
```

This connects to Chrome on :9228, drives the x.com search results page for AI-monetization queries, scrolls to load more tweets, and deduplicates against `scripts/scrapers_x/data/x.sqlite3`.

### Step 2: Identify candidates

From the SQLite `tweets` table, pick posts whose `last_seen_at` is within the last 24 hours, sorted by engagement score:

```sql
SELECT tweet_id, posted_at, author_handle, likes, replies, quotes, reposts,
       substr(body_text, 1, 200) AS preview
FROM tweets
WHERE last_seen_at >= datetime('now', '-1 day')
  AND last_seen_at != first_seen_at
  AND body_text IS NOT NULL
ORDER BY (coalesce(likes,0)*2 + coalesce(replies,0)*3 + coalesce(quotes,0)*2 + coalesce(reposts,0)*1) DESC
LIMIT 30
```

Score formula: `likes*2 + replies*3 + quotes*2 + reposts`. Replies weighted highest because they signal deeper engagement than a like.

### Step 3: Filter to AI-related cases

For each candidate, scan the body text for the AI keyword list (`references/keyword_list.md`). Drop posts that are pure technical-help ("how do I configure X"), pure social-media banter, or non-AI topic niches.

### Step 4: Rank and cap at 5

Keep candidates with engagement score ≥ 6. Take top 5 by score. Tiebreak on `posted_at DESC` (fresher wins).

If zero candidates pass, abort with "no AI-related candidates since last run; nothing to draft."

### Step 5: For each candidate, draft

For each passing candidate, write the bilingual blog post. The schema lives in `references/blog_schema.md` and the tone reference is `references/tone_guide.md`.

The body section names are: `## Context`, `## Numbers`, `## Cost structure`, `## What this case does not cover`, `## Take-away`.

**No source footer.** Do NOT add a `**Source**: linked from...` block. The post reads as if the writer is documenting the case directly. Provenance (tweet_id, author_handle) stays in `scripts/scrapers_x/data/x.sqlite3`.

### Step 6: Final report

Print a summary block:

```
twitter-x-daily-blog: 4 drafts created
- src/content/blog/<slug-1>/{en,zh}.md
- src/content/blog/<slug-2>/{en,zh}.md
- src/content/blog/<slug-3>/{en,zh}.md
- src/content/blog/<slug-4>/{en,zh}.md

Run `pnpm build` to confirm all drafts compile. The drafts are NOT committed; run `git status` and pick the ones you want.
```

Stop after the summary. Do NOT run `git add` or `git commit`. That is the user's call.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| CDP health check fails | Chrome not debugging on :9228 | Print remediation, abort |
| Scraper import fails | `_lib/` python files are missing or syntax-broken | Print remediation, abort |
| No candidates with score ≥ 6 | Today's pulls have low engagement OR non-AI content | Abort with "nothing AI-related to draft today" |
| Existing `<slug>` directory exists | Today's slug collides with an old slug | Add a date suffix `<slug>-2026-07-04` |
| Build fails after drafting | Schema error in frontmatter, broken UTF-8, etc. | Print the build error verbatim. Continue or abort at your discretion — typically fix the offending file and rerun build. |
| x.com returns login wall | User not logged in to x.com in the :9228 Chrome | Ask user to log in, then rerun |

## What this skill does NOT do

- Never calls any external API. ANTHROPIC_API_KEY is not required and not used.
- Never commits, pushes, opens PRs, or modifies git state.
- Never edits posts that already exist in `src/content/blog/`.
- Never touches the scraper source code under `scripts/scrapers_x/`.

## References

See `references/keyword_list.md`, `references/blog_schema.md`, and `references/tone_guide.md` for input detail used by Step 5.
