# Twitter/X AI-monetization daily blog skill — Design

**Date:** 2026-07-02
**Skill name:** `twitter-x-daily-blog`
**Status:** Approved — pending implementation plan

## 1. Purpose

Surface real-world AI-monetization patterns from public X (Twitter) posts and
turn them into the same bilingual blog drafts the existing
`zsxq-daily-blog` skill produces for the AI Lab section. The output is
identical in shape to the knowledge-planet pipeline: cold-eyed case-study
markdown with frontmatter, six FAQs, math-driven body, and no source
attribution in the published file.

The two skills target the same editorial outcome from two different
upstream sources. They share design language but not code.

## 2. Architecture overview

```
.claude/skills/twitter-x-daily-blog/
├── SKILL.md                          # skill entry, conversational invoke
└── references/
    ├── blog_schema.md                # frontmatter + body rules (mirror zsxq)
    ├── keyword_list.md               # AI keyword filter (mirror zsxq)
    └── tone_guide.md                 # writing voice (mirror zsxq)

scripts/scrapers_x/                   # sibling to scripts/scrapers/
├── crawl.py                          # attach → scroll → persist
├── probe.py                          # one-shot health probe of :9228
├── _lib/
│   ├── __init__.py
│   ├── cdp.py                        # attach + reuse/find x.com tab
│   ├── db.py                         # SQLite: topics, runs
│   └── selectors.py                  # search URLs, DOM selectors
├── tests/
│   ├── test_db.py
│   ├── test_selectors.py
│   └── test_score.py
└── data/
    └── x.sqlite3                     # runtime, gitignored
```

The `scrapers_x/` tree mirrors `scrapers/` but stays physically separate.
Two reasons:

1. **Port contract.** Twitter lives on `:9228`, knowledge-planet on `:9225`.
   Sharing a `_lib/cdp.py` would mean every call site has to remember which
   port to use. Two files, two defaults — less to mis-wire.
2. **Failure isolation.** If a Twitter session gets rate-limited or the
   X.com selectors break, the zsxq pipeline keeps running.

The skill files (`SKILL.md`, `references/*.md`) **do** mirror zsxq's
structure, and may duplicate content if that's clearer than referencing
across the boundary. The references are short.

## 3. Data model

### `topics` table

```sql
CREATE TABLE topics (
  tweet_id        TEXT PRIMARY KEY,         -- last numeric segment of URL
  url             TEXT NOT NULL UNIQUE,     -- https://x.com/<handle>/status/<id>
  author_handle   TEXT,
  author_name     TEXT,
  posted_at       TEXT,                     -- ISO-8601, may be null if X renders nothing
  body_text       TEXT NOT NULL,
  like_count      INTEGER,
  reply_count     INTEGER,
  repost_count    INTEGER,
  quote_count     INTEGER,
  search_keyword  TEXT,                     -- which keyword triggered this row
  search_mode     TEXT,                     -- 'top' | 'live'
  first_seen_at   TEXT NOT NULL,            -- ISO-8601 UTC
  last_seen_at    TEXT NOT NULL             -- ISO-8601 UTC
);
CREATE UNIQUE INDEX idx_topics_url ON topics(url);
```

### `runs` table

Same shape as `scrapers/_lib/db.py`. Fields: `run_id`, `mode`, `started_at`,
`finished_at`, `status`, `items_seen`, `items_inserted`, `items_skipped`.

### Persistence contract

- All timestamps are ISO-8601 UTC (`%Y-%m-%dT%H:%M:%SZ`).
- Every SQL uses `?` placeholders. No f-string SQL.
- `INSERT OR IGNORE` so the URL UNIQUE constraint is the de-dupe mechanism.
- Foreign keys enabled.

## 4. Crawl flow

```
for mode in ['top', 'live']:
    page.goto(SEARCH_URLS[mode])
    for round in range(SCROLL_ROUNDS):           # default 5
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(random(800, 1400))
    for article in page.query_selector_all('article[data-testid="tweet"]'):
        row = parse_tweet(article, mode)
        db.topics.insert_or_ignore(row)
```

### Search URLs

```
TOP  : https://x.com/search?q=AI%E5%8F%98%E7%8E%B0&src=typed_query
LIVE : https://x.com/search?q=AI%E5%8F%98%E7%8E%B0&src=typed_query&f=live
```

Both are read from `selectors.SEARCH_URLS` so the keyword can be swapped
in one place without touching `crawl.py`.

### DOM selectors (initial probe targets)

| Field | Selector |
|---|---|
| Tweet root | `article[data-testid="tweet"]` |
| Tweet URL | `a[href*="/status/"]` (first descendant) |
| Tweet text | `[data-testid="tweetText"]` |
| Author handle | `[data-testid="User-Name"]` text content |
| Like count | `[data-testid="like"]` ancestor `button[aria-label]` |
| Reply count | `[data-testid="reply"]` ancestor `button[aria-label]` |
| Repost count | `[data-testid="retweet"]` ancestor `button[aria-label]` |

Aria-label parsing regex: `r"^([\d,.]+)([KMB]?)"` → multiply by 1k/1M/1B.
The selector list lives in `selectors.py` as a single `DOM_SELECTORS`
dict so the probe can update it without code review.

### Scroll policy

- 5 rounds max per page.
- Per-round `wait_for_timeout(random(800, 1400))`.
- Hard timeout 30 s per `goto`.
- If a round returns zero new articles, abort the current page early.

### Tab policy

- Reuse any open `x.com` tab in the user's Chrome.
- If none, open exactly one new tab in the default context, navigate,
  and close it on exit. Existing zsxq tab is left alone.

## 5. Candidate filter

Run from inside SKILL.md's Step 4:

```sql
SELECT *,
       (coalesce(like_count,0)*2
        + coalesce(reply_count,0)*3
        + coalesce(quote_count,0)*2
        + coalesce(repost_count,0)) AS score
FROM topics
WHERE last_seen_at >= datetime('now', '-1 day')
  AND last_seen_at = first_seen_at
  AND body_text LIKE '%AI%'
     OR body_text LIKE '%GPT%'
     OR body_text LIKE '%Claude%'
     OR body_text LIKE '%LLM%'
     OR body_text LIKE '%agent%'
     OR body_text LIKE '%智能体%'
     OR body_text LIKE '%Seedance%'
     OR body_text LIKE '%Sora%'
     OR body_text LIKE '%Midjourney%'
     OR body_text LIKE '%ComfyUI%'
     OR body_text LIKE '%Cursor%'
     OR body_text LIKE '%提示词%'
     OR body_text LIKE '%模型%'
ORDER BY score DESC, posted_at DESC
LIMIT 5;
```

Threshold: `score >= 6`. If fewer than one candidate passes, the skill
aborts with "no AI-related candidates since last run; nothing to draft"
and writes nothing.

The keyword list mirrors `zsxq-daily-blog/references/keyword_list.md`.
If the two diverge later, keep them diverged — each skill owns its own
list.

## 6. Draft generation

For each candidate, draft a bilingual blog post. Schema mirrors
`zsxq-daily-blog/references/blog_schema.md`:

```yaml
---
title: 'Sentence-case headline'
description: '80-160 char subtitle, math-driven when possible'
pubDate: YYYY-MM-DD
category: 'ai'
tags: ['ai', '<niche>', 'case-study', 'monetization']
translationKey: '<slug>'
tldr: '1-2 sentence summary'
faq:
  - q: '...'; a: '...'
  ... (exactly 6)
---
```

Body sections (in order): `## Context` → `## Numbers` →
`## Cost structure` → `## What this case does not cover` →
`## Take-away`.

### Hard rules (carry over from zsxq tone_guide.md)

- No source footer. Provenance lives only in SQLite.
- No author / handle / post URL in the published file.
- Numbers always carry units.
- Every post lists 3-5 honest gaps.

### Slug rule

- kebab-case, 3-6 words, no number at start.
- Examples: `x-ai-prompt-store`, `x-claude-agent-launch`, `x-ai-saas-pricing`.
- Conflict with an existing folder → append `-YYYY-MM-DD`.

## 7. Error handling

| Symptom | Action |
|---|---|
| `curl :9228/json/version` fails | abort; print one-line remediation |
| `_lib` import fails | abort; print path-missing message |
| Search page returns 0 articles | warn, skip that mode, continue with the other |
| Tweet root selector finds nothing | abort; selectors likely need probe |
| `tweetText` selector missing on a card | skip card, continue |
| URL parse fails | skip card, continue |
| `like/reply/repost` aria-label missing | record `0` for that field, do not skip |
| CDP connection drops mid-crawl | abort; do not retry |
| SQLite UNIQUE collision | silent skip — that's the de-dupe |
| All candidates filtered out | abort with "nothing AI-related to draft today" |

## 8. Testing

`pytest` only — no E2E. Twitter's anti-bot stance makes headless tests
brittle and slow.

| Module | Test surface |
|---|---|
| `_lib/db.py` | UNIQUE constraint, URL → tweet_id extraction, ISO timestamp round-trip, `record_run_*` lifecycle |
| `_lib/selectors.py` | Parse static HTML fixture for each selector; aria-label regex (`1.2K`, `12`, `1M`) |
| score function | Pure unit test of the SQL expression logic in Python |
| `crawl.py` argparse | CLI flags, `--dry-run`, `--scroll-rounds` |

Coverage target ≥ 80% (`pytest --cov=scripts/scrapers_x`).

`probe.py` is a manual-run script, not part of the test suite. It opens
one search page, prints the first five tweet URLs, exits.

## 9. Out of scope

- Logging in / handling credentials. The user's Chrome is already
  authenticated to X.com. We never touch credentials.
- Storing or transmitting tweet text to any external API. The skill
  writes to local SQLite only.
- Any automatic push to git. Like zsxq-daily-blog, the operator decides
  what to commit.
- Editing existing blog posts.
- Tweet replies/threads. Each `article[data-testid="tweet"]` is one row;
  thread context is not joined.

## 10. References

- `scripts/scrapers/` — sibling scraper, design template
- `.claude/skills/zsxq-daily-blog/` — sibling skill, blog schema source
- `docs/superpowers/specs/2026-06-30-zsxq-daily-blog-design.md` — original
  spec (if it exists)