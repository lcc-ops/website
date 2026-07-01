# twitter-x-daily-blog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude skill `twitter-x-daily-blog` that crawls public X.com search results for AI-monetization posts, deduplicates against a local SQLite, and drafts bilingual AI Lab blog posts identical in shape to the existing `zsxq-daily-blog` output.

**Architecture:** Skill entry at `.claude/skills/twitter-x-daily-blog/SKILL.md` invokes a Python scraper at `scripts/scrapers_x/crawl.py`. The scraper attaches to the user's Chrome via CDP on `localhost:9228` (a separate Chrome instance from zsxq's `:9225`), scrolls two search results pages (top + live), extracts `article[data-testid="tweet"]` cards, and persists them to `scripts/scrapers_x/data/x.sqlite3` with URL as the unique key. The skill's Step 4-6 query the SQLite for 24h-new AI-keyword candidates, score them by interaction, and emit `src/content/blog/<slug>/{en,zh}.md` files matching the AI Lab schema.

**Tech Stack:** Python 3.11+, Playwright sync API, SQLite, pytest, ruff, mypy. No external HTTP client libraries — the scraper talks only to the user's Chrome via CDP.

---

## File Structure

```
.claude/skills/twitter-x-daily-blog/
├── SKILL.md                              # skill entry
└── references/
    ├── blog_schema.md                    # mirrors zsxq
    ├── keyword_list.md                   # mirrors zsxq
    └── tone_guide.md                     # mirrors zsxq

scripts/scrapers_x/
├── crawl.py                              # CLI: --mode auto|full|incremental
├── probe.py                              # manual health probe of :9228
├── _lib/
│   ├── __init__.py                       # empty marker
│   ├── cdp.py                            # attach_chrome, scoped_chrome, x.com tab logic
│   ├── db.py                             # Database, TopicRow, RunSummary, utcnow_iso
│   └── selectors.py                      # SEARCH_URLS, DOM_SELECTORS, parse_count()
├── tests/
│   ├── __init__.py                       # empty marker
│   ├── conftest.py                       # tmp SQLite fixture
│   ├── test_db.py                        # UNIQUE, URL parse, ISO round-trip
│   ├── test_selectors.py                 # aria-label regex, URL parse
│   └── test_score.py                     # pure score function
└── data/
    └── .gitignore                        # ignore *.sqlite3*
```

---

## Task 1: Skill scaffold

**Files:**
- Create: `.claude/skills/twitter-x-daily-blog/SKILL.md`
- Create: `.claude/skills/twitter-x-daily-blog/references/blog_schema.md`
- Create: `.claude/skills/twitter-x-daily-blog/references/keyword_list.md`
- Create: `.claude/skills/twitter-x-daily-blog/references/tone_guide.md`

- [ ] **Step 1: Create SKILL.md**

Write the skill entry. The body describes the 6-step pipeline: CDP pre-flight → crawl → read SQLite → filter → score → draft bilingual posts. Mirror `zsxq-daily-blog/SKILL.md` structure exactly. Use frontmatter:

```markdown
---
name: twitter-x-daily-blog
description: Use when the user asks to "pull today's X/Twitter AI-monetization posts and write them up" or invokes @twitter-x-daily-blog. Mirrors zsxq-daily-blog but reads from x.com search results via the user's Chrome on CDP :9228.
---

# twitter-x-daily-blog

This skill turns a fresh pull of X.com search results for AI-monetization
posts into bilingual blog drafts for the project's AI Lab section.

## When to invoke

Trigger on any of:
- "pull today's X AI-monetization posts and write them up"
- "do the daily X pass"
- "refresh twitter and turn it into blog posts"
- the user explicitly invokes `@twitter-x-daily-blog`

Do NOT invoke for:
- ad-hoc single-topic writing
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

### Step 1: Run the crawl

```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode auto --scroll-rounds 5 --humane-delay-ms 800 1400
```

Capture the run's output, especially the new `runs.mode`, `runs.items_inserted`, `runs.items_skipped` rows.

### Step 2: Read what came in

```sql
SELECT tweet_id, url, author_handle, posted_at, like_count, reply_count,
       repost_count, quote_count, search_mode,
       substr(body_text, 1, 200) AS preview
FROM topics
WHERE last_seen_at >= datetime('now', '-1 day')
  AND last_seen_at = first_seen_at
  AND body_text IS NOT NULL
ORDER BY (coalesce(like_count,0)*2
        + coalesce(reply_count,0)*3
        + coalesce(quote_count,0)*2
        + coalesce(repost_count,0)) DESC
LIMIT 30;
```

### Step 3: Filter to AI-related cases

For each candidate, scan the body text against `references/keyword_list.md`.
Drop posts that are pure technical help, pure social-media admin questions,
or non-AI topic niches.

### Step 4: Rank and cap at 5

Score = `(likes * 2) + (replies * 3) + (quotes * 2) + reposts`. Take top 5 by score.
Tiebreak on `posted_at DESC` (fresher wins). Drop any candidate with `score < 6`.

If zero candidates pass, abort with "no AI-related candidates since last run; nothing to draft."

### Step 5: For each candidate, draft

Write a bilingual blog post matching the schema in `references/blog_schema.md`.
The tone is governed by `references/tone_guide.md`.

**Slug rule**: lowercase, dashes, kebab-case; 3-6 words; use the case's main
keyword (`x-ai-prompt-store`, `x-claude-agent-launch`). Translate
`translationKey` to the same string.

**Frontmatter required fields** (matches existing AI Lab posts):

```yaml
---
title: "..."
description: "..."
pubDate: <today, e.g. 2026-07-02>
category: 'ai'
tags: ['ai', '<one-of-vertical-niche>', 'case-study', 'monetization']
translationKey: '<slug>'
tldr: "..."
faq:
  - q: "..."; a: "..."
  ... (exactly 6 entries)
---
```

### Step 6: Final report

Print:

```
twitter-x-daily-blog: N drafts created
- src/content/blog/<slug-1>/{en,zh}.md
- ...

Run `pnpm build` to confirm all compile. The drafts are NOT committed; run `git status` and pick the ones you want.
```

Stop after the summary. Do NOT run `git add` or `git commit`.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| CDP health check fails | Chrome not debugging on :9228 | Print remediation, abort |
| Scraper import fails | `_lib/` python files are missing | Print remediation, abort |
| No candidates with score ≥ 6 | Today's pulls have low interaction OR non-AI content | Abort with "nothing AI-related to draft today" |
| Existing `<slug>` directory exists | Today's slug collides with an old slug | Add a date suffix `<slug>-2026-07-02` |
| Build fails after drafting | Schema error in frontmatter, broken UTF-8, etc. | Print the build error verbatim |

## What this skill does NOT do

- Never calls any external API. No credentials stored.
- Never commits, pushes, opens PRs, or modifies git state.
- Never edits posts that already exist in `src/content/blog/`.
- Never touches the existing `scripts/scrapers/` source code.
```

- [ ] **Step 2: Create references/blog_schema.md**

Mirror the structure of `.claude/skills/zsxq-daily-blog/references/blog_schema.md` exactly. Replace any `src/content/blog/<slug>/{en,zh}.md` examples but keep the YAML frontmatter template, body section ordering (Context → Numbers → Cost structure → What this case does not cover → Take-away), slug rule, and the no-source-footer rule.

- [ ] **Step 3: Create references/keyword_list.md**

Copy verbatim from `.claude/skills/zsxq-daily-blog/references/keyword_list.md` into `.claude/skills/twitter-x-daily-blog/references/keyword_list.md`. The keyword list is identical because both skills filter for the same AI Lab topic.

- [ ] **Step 4: Create references/tone_guide.md**

Copy verbatim from `.claude/skills/zsxq-daily-blog/references/tone_guide.md`. The writing voice is identical.

- [ ] **Step 5: Verify skill loads**

Run:
```bash
ls -la .claude/skills/twitter-x-daily-blog/
ls -la .claude/skills/twitter-x-daily-blog/references/
```

Expected: 1 SKILL.md and 3 references files exist. No build step needed.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/twitter-x-daily-blog/
git commit -m "feat(skill): scaffold twitter-x-daily-blog"
```

---

## Task 2: Project scaffold for the scraper

**Files:**
- Create: `scripts/scrapers_x/_lib/__init__.py`
- Create: `scripts/scrapers_x/tests/__init__.py`
- Create: `scripts/scrapers_x/data/.gitignore`
- Create: `pyproject.toml` (add a `[tool.pytest.ini_options]` section only)

- [ ] **Step 1: Create `_lib/__init__.py`**

Empty file. This is the marker that makes `from _lib import ...` work when
the repo root is on `sys.path`.

```python
# scripts/scrapers_x/_lib/__init__.py
```

- [ ] **Step 2: Create `tests/__init__.py`**

Empty file.

```python
# scripts/scrapers_x/tests/__init__.py
```

- [ ] **Step 3: Create `data/.gitignore`**

```
*.sqlite3
*.sqlite3-shm
*.sqlite3-wal
```

- [ ] **Step 4: Add pytest config to `pyproject.toml`**

Open `pyproject.toml` at the repo root. If it does not exist, create a
minimal one. Append (do not overwrite existing config):

```toml
[tool.pytest.ini_options]
testpaths = ["scripts/scrapers_x/tests"]
addopts = "-ra --strict-markers"
```

- [ ] **Step 5: Verify pytest can collect (even with zero tests)**

Run:
```bash
cd <repo-root>
python -m pytest scripts/scrapers_x/tests --collect-only
```

Expected: `no tests ran` or `collected 0 items`. No import errors.

- [ ] **Step 6: Commit**

```bash
git add scripts/scrapers_x/ pyproject.toml
git commit -m "feat(scrapers_x): scaffold _lib and tests"
```

---

## Task 3: Time helpers in `_lib/db.py` (TDD)

**Files:**
- Create: `scripts/scrapers_x/_lib/db.py`
- Test: `scripts/scrapers_x/tests/test_db.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/scrapers_x/tests/test_db.py
from datetime import datetime, timezone

from _lib.db import utcnow_iso, now_minus_seconds_iso


def test_utcnow_iso_format():
    """ISO-8601 UTC string ending in Z with second precision."""
    s = utcnow_iso()
    # 2026-07-02T12:34:56Z
    assert s.endswith("Z")
    assert len(s) == 20
    parsed = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    assert parsed.tzinfo is not None


def test_now_minus_seconds_iso():
    """3600 seconds earlier than now."""
    s = now_minus_seconds_iso(3600)
    parsed = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - parsed
    # allow 5s drift for slow tests
    assert 3595 <= delta.total_seconds() <= 3605
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py -v`
Expected: `ModuleNotFoundError: No module named '_lib.db'`

- [ ] **Step 3: Write the implementation**

```python
# scripts/scrapers_x/_lib/db.py
"""SQLite persistence for the X.com scraper.

Public surface (grows across later tasks):

    db = Database.open(path)
    db.ensure_schema()
    run_id = db.record_run_start(mode='full', started_at=...)
    db.record_run_end(run_id, status='ok', items_seen=..., ...)
    if db.topics.exists(tweet_id): ...
    db.topics.upsert(tweet_row)   # URL UNIQUE → INSERT OR IGNORE
    db.topics.touch_last_seen(tweet_id, last_seen_at_iso)

Design choices mirror scripts/scrapers/_lib/db.py:
- All timestamps are ISO-8601 UTC strings ending in 'Z'.
- Every SQL uses '?' placeholders. No f-string SQL.
- Foreign keys are enabled.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def utcnow_iso() -> str:
    """ISO-8601 UTC string with second precision and trailing Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_minus_seconds_iso(seconds: int) -> str:
    """ISO-8601 UTC string for ``seconds`` ago."""
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/_lib/db.py scripts/scrapers_x/tests/test_db.py
git commit -m "feat(scrapers_x): add time helpers"
```

---

## Task 4: Database class — schema + topics table (TDD)

**Files:**
- Modify: `scripts/scrapers_x/_lib/db.py`
- Modify: `scripts/scrapers_x/tests/test_db.py`
- Create: `scripts/scrapers_x/tests/conftest.py`

- [ ] **Step 1: Write the failing tests**

Append to `scripts/scrapers_x/tests/test_db.py`:

```python
import pytest

from _lib.db import Database, TopicRow


@pytest.fixture
def db(tmp_path):
    """Fresh SQLite for each test."""
    path = tmp_path / "x.sqlite3"
    database = Database.open(path)
    database.ensure_schema()
    return database


def test_database_creates_schema(db, tmp_path):
    """Tables topics and runs exist after ensure_schema."""
    import sqlite3
    with sqlite3.connect(tmp_path / "x.sqlite3") as c:
        names = {row[0] for row in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert "topics" in names
    assert "runs" in names


def test_topics_unique_url(db):
    """Two rows with the same URL → second is ignored."""
    row = TopicRow(
        tweet_id="100",
        url="https://x.com/a/status/100",
        author_handle="a",
        author_name="A",
        posted_at=None,
        body_text="hello",
        like_count=1,
        reply_count=0,
        repost_count=0,
        quote_count=0,
        search_keyword="AI变现",
        search_mode="top",
        first_seen_at="2026-07-02T00:00:00Z",
        last_seen_at="2026-07-02T00:00:00Z",
    )
    db.topics.upsert(row)
    db.topics.upsert(row)  # same url, ignored
    rows = db.topics.recent(within_seconds=86400)
    assert len(rows) == 1


def test_topics_recent_orders_by_last_seen(db):
    """recent() returns rows newest-first by last_seen_at."""
    older = TopicRow(
        tweet_id="1", url="https://x.com/a/status/1",
        author_handle="a", author_name="A", posted_at=None,
        body_text="old", like_count=0, reply_count=0,
        repost_count=0, quote_count=0,
        search_keyword="AI变现", search_mode="top",
        first_seen_at="2026-07-01T00:00:00Z",
        last_seen_at="2026-07-01T00:00:00Z",
    )
    newer = TopicRow(
        tweet_id="2", url="https://x.com/b/status/2",
        author_handle="b", author_name="B", posted_at=None,
        body_text="new", like_count=0, reply_count=0,
        repost_count=0, quote_count=0,
        search_keyword="AI变现", search_mode="live",
        first_seen_at="2026-07-02T00:00:00Z",
        last_seen_at="2026-07-02T00:00:00Z",
    )
    db.topics.upsert(older)
    db.topics.upsert(newer)
    rows = db.topics.recent(within_seconds=86400 * 2)
    assert [r.tweet_id for r in rows] == ["2", "1"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py -v`
Expected: ImportError for `Database` and `TopicRow` (or AttributeError on db.topics.upsert).

- [ ] **Step 3: Add TopicRow and Database class to `_lib/db.py`**

Replace the contents of `scripts/scrapers_x/_lib/db.py` with:

```python
"""SQLite persistence for the X.com scraper."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_minus_seconds_iso(seconds: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


@dataclass(frozen=True)
class TopicRow:
    tweet_id: str
    url: str
    author_handle: Optional[str]
    author_name: Optional[str]
    posted_at: Optional[str]
    body_text: str
    like_count: int
    reply_count: int
    repost_count: int
    quote_count: int
    search_keyword: str
    search_mode: str
    first_seen_at: str
    last_seen_at: str


class _Topics:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._c = conn

    def upsert(self, row: TopicRow) -> None:
        """INSERT OR IGNORE on tweet_id; always bump last_seen_at."""
        self._c.execute(
            """
            INSERT OR IGNORE INTO topics (
              tweet_id, url, author_handle, author_name, posted_at,
              body_text, like_count, reply_count, repost_count, quote_count,
              search_keyword, search_mode, first_seen_at, last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.tweet_id, row.url, row.author_handle, row.author_name,
                row.posted_at, row.body_text,
                row.like_count, row.reply_count, row.repost_count, row.quote_count,
                row.search_keyword, row.search_mode,
                row.first_seen_at, row.last_seen_at,
            ),
        )
        self._c.execute(
            "UPDATE topics SET last_seen_at = ? WHERE tweet_id = ?",
            (row.last_seen_at, row.tweet_id),
        )
        self._c.commit()

    def recent(self, within_seconds: int) -> list[TopicRow]:
        """Rows whose last_seen_at is within the window, newest first."""
        from .db import now_minus_seconds_iso
        cutoff = now_minus_seconds_iso(within_seconds)
        cur = self._c.execute(
            """
            SELECT tweet_id, url, author_handle, author_name, posted_at,
                   body_text, like_count, reply_count, repost_count,
                   quote_count, search_keyword, search_mode,
                   first_seen_at, last_seen_at
            FROM topics
            WHERE last_seen_at >= ?
            ORDER BY last_seen_at DESC
            """,
            (cutoff,),
        )
        return [TopicRow(*row) for row in cur.fetchall()]


class Database:
    def __init__(self, conn: sqlite3.Connection, path: Path) -> None:
        self._c = conn
        self._path = path
        self.topics = _Topics(conn)

    @classmethod
    def open(cls, path: Path) -> "Database":
        conn = sqlite3.connect(path)
        conn.execute("PRAGMA foreign_keys = ON")
        return cls(conn, path)

    def ensure_schema(self) -> None:
        self._c.executescript(
            """
            CREATE TABLE IF NOT EXISTS topics (
              tweet_id        TEXT PRIMARY KEY,
              url             TEXT NOT NULL UNIQUE,
              author_handle   TEXT,
              author_name     TEXT,
              posted_at       TEXT,
              body_text       TEXT NOT NULL,
              like_count      INTEGER NOT NULL DEFAULT 0,
              reply_count     INTEGER NOT NULL DEFAULT 0,
              repost_count    INTEGER NOT NULL DEFAULT 0,
              quote_count     INTEGER NOT NULL DEFAULT 0,
              search_keyword  TEXT NOT NULL,
              search_mode     TEXT NOT NULL,
              first_seen_at   TEXT NOT NULL,
              last_seen_at    TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_topics_last_seen
              ON topics(last_seen_at);
            """
        )
        self._c.commit()

    def close(self) -> None:
        self._c.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py -v`
Expected: 5 passed (2 from Task 3 + 3 from this task).

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/_lib/db.py scripts/scrapers_x/tests/test_db.py
git commit -m "feat(scrapers_x): database class + topics table"
```

---

## Task 5: Runs table (TDD)

**Files:**
- Modify: `scripts/scrapers_x/_lib/db.py`
- Modify: `scripts/scrapers_x/tests/test_db.py`

- [ ] **Step 1: Write the failing tests**

Append to `scripts/scrapers_x/tests/test_db.py`:

```python
def test_runs_lifecycle(db):
    """record_run_start returns an id; record_run_end finalizes it."""
    from _lib.db import utcnow_iso
    started = utcnow_iso()
    run_id = db.record_run_start(mode="full", started_at=started)
    assert isinstance(run_id, int)
    db.record_run_end(
        run_id,
        finished_at=utcnow_iso(),
        status="ok",
        items_seen=10,
        items_inserted=7,
        items_skipped=3,
    )
    summary = db.last_successful_run()
    assert summary is not None
    assert summary.mode == "full"
    assert summary.items_inserted == 7
    assert summary.items_skipped == 3


def test_runs_skips_non_ok(db):
    """last_successful_run ignores failed runs."""
    from _lib.db import utcnow_iso
    now = utcnow_iso()
    bad = db.record_run_start(mode="full", started_at=now)
    db.record_run_end(
        bad, finished_at=utcnow_iso(), status="error",
        items_seen=0, items_inserted=0, items_skipped=0,
    )
    assert db.last_successful_run() is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py::test_runs_lifecycle scripts/scrapers_x/tests/test_db.py::test_runs_skips_non_ok -v`
Expected: AttributeError on `record_run_start` / `last_successful_run`.

- [ ] **Step 3: Add runs support to `_lib/db.py`**

Append a `runs` table to `ensure_schema`, and the lifecycle methods on `Database`. Update the `ensure_schema` method in `db.py`:

```python
    def ensure_schema(self) -> None:
        self._c.executescript(
            """
            CREATE TABLE IF NOT EXISTS topics (
              tweet_id        TEXT PRIMARY KEY,
              url             TEXT NOT NULL UNIQUE,
              author_handle   TEXT,
              author_name     TEXT,
              posted_at       TEXT,
              body_text       TEXT NOT NULL,
              like_count      INTEGER NOT NULL DEFAULT 0,
              reply_count     INTEGER NOT NULL DEFAULT 0,
              repost_count    INTEGER NOT NULL DEFAULT 0,
              quote_count     INTEGER NOT NULL DEFAULT 0,
              search_keyword  TEXT NOT NULL,
              search_mode     TEXT NOT NULL,
              first_seen_at   TEXT NOT NULL,
              last_seen_at    TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_topics_last_seen
              ON topics(last_seen_at);

            CREATE TABLE IF NOT EXISTS runs (
              run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
              mode            TEXT NOT NULL,
              started_at      TEXT NOT NULL,
              finished_at     TEXT,
              status          TEXT NOT NULL DEFAULT 'in_progress',
              items_seen      INTEGER NOT NULL DEFAULT 0,
              items_inserted  INTEGER NOT NULL DEFAULT 0,
              items_skipped   INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_runs_status
              ON runs(status);
            """
        )
        self._c.commit()

    def record_run_start(self, mode: str, started_at: str) -> int:
        cur = self._c.execute(
            "INSERT INTO runs(mode, started_at) VALUES (?, ?)",
            (mode, started_at),
        )
        self._c.commit()
        return cur.lastrowid

    def record_run_end(
        self,
        run_id: int,
        finished_at: str,
        status: str,
        items_seen: int,
        items_inserted: int,
        items_skipped: int,
    ) -> None:
        self._c.execute(
            """
            UPDATE runs
               SET finished_at = ?, status = ?,
                   items_seen = ?, items_inserted = ?, items_skipped = ?
             WHERE run_id = ?
            """,
            (
                finished_at, status,
                items_seen, items_inserted, items_skipped,
                run_id,
            ),
        )
        self._c.commit()

    def last_successful_run(self) -> Optional["RunSummary"]:
        from _lib.db import RunSummary
        cur = self._c.execute(
            """
            SELECT run_id, mode, started_at, finished_at, status,
                   items_seen, items_inserted, items_skipped
              FROM runs
             WHERE status = 'ok'
             ORDER BY started_at DESC
             LIMIT 1
            """
        )
        row = cur.fetchone()
        if row is None:
            return None
        return RunSummary(*row)
```

Also add `RunSummary` dataclass at the top of `db.py`:

```python
@dataclass(frozen=True)
class RunSummary:
    run_id: int
    mode: str
    started_at: str
    finished_at: Optional[str]
    status: str
    items_seen: int
    items_inserted: int
    items_skipped: int
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_db.py -v`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/_lib/db.py scripts/scrapers_x/tests/test_db.py
git commit -m "feat(scrapers_x): runs table lifecycle"
```

---

## Task 6: URL and aria-label helpers in `selectors.py` (TDD)

**Files:**
- Create: `scripts/scrapers_x/_lib/selectors.py`
- Test: `scripts/scrapers_x/tests/test_selectors.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/scrapers_x/tests/test_selectors.py
import pytest

from _lib.selectors import (
    SEARCH_URLS,
    parse_tweet_id,
    parse_count,
)


def test_search_urls_contains_top_and_live():
    assert "top" in SEARCH_URLS
    assert "live" in SEARCH_URLS
    assert "AI%E5%8F%98%E7%8E%B0" in SEARCH_URLS["top"]
    assert "f=live" in SEARCH_URLS["live"]


@pytest.mark.parametrize("url,expected", [
    ("https://x.com/foo/status/1234567890", "1234567890"),
    ("https://twitter.com/bar/status/42", "42"),
    ("https://x.com/baz/status/999999999999999999", "999999999999999999"),
])
def test_parse_tweet_id(url, expected):
    assert parse_tweet_id(url) == expected


def test_parse_tweet_id_invalid():
    assert parse_tweet_id("https://example.com/foo") is None
    assert parse_tweet_id("not a url") is None


@pytest.mark.parametrize("label,expected", [
    ("12", 12),
    ("1.2K", 1200),
    ("12K", 12000),
    ("1.5M", 1_500_000),
    ("2.3B", 2_300_000_000),
    ("1,234", 1234),
    ("Like", 0),  # unknown → 0
    ("", 0),
])
def test_parse_count(label, expected):
    assert parse_count(label) == expected
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_selectors.py -v`
Expected: `ModuleNotFoundError: No module named '_lib.selectors'`

- [ ] **Step 3: Write the implementation**

```python
# scripts/scrapers_x/_lib/selectors.py
"""Constants and DOM helpers for the X.com scraper.

The two contracts:

1. SEARCH_URLS — the two search result pages the crawler visits. Change
   the keyword here, not in crawl.py.

2. parse_tweet_id / parse_count — pure functions for extracting fields
   from rendered DOM strings. Unit-tested with no Playwright dependency.
"""

from __future__ import annotations

import re
from typing import Optional

# ---------------------------------------------------------------------------
# Search URLs. UPDATE KEYWORD HERE.
# ---------------------------------------------------------------------------
SEARCH_KEYWORD: str = "AI变现"
_ENCODED: str = "AI%E5%8F%98%E7%8E%B0"  # "AI变现" URL-encoded

SEARCH_URLS: dict[str, str] = {
    "top": f"https://x.com/search?q={_ENCODED}&src=typed_query",
    "live": f"https://x.com/search?q={_ENCODED}&src=typed_query&f=live",
}

# ---------------------------------------------------------------------------
# DOM selectors (initial; the probe may update these)
# ---------------------------------------------------------------------------
DOM_SELECTORS: dict[str, str] = {
    "tweet_root": 'article[data-testid="tweet"]',
    "tweet_url": 'a[href*="/status/"]',
    "tweet_text": '[data-testid="tweetText"]',
    "user_name": '[data-testid="User-Name"]',
    "like_button": '[data-testid="like"]',
    "reply_button": '[data-testid="reply"]',
    "retweet_button": '[data-testid="retweet"]',
}

# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------
_TWEET_ID_RE = re.compile(r"/status/(\d+)")


def parse_tweet_id(url: str) -> Optional[str]:
    """Extract the numeric tweet id from an x.com / twitter.com URL.

    Returns None if the URL has no /status/<digits> segment.
    """
    if not url:
        return None
    m = _TWEET_ID_RE.search(url)
    if m is None:
        return None
    return m.group(1)


_COUNT_RE = re.compile(r"^([\d,.]+)\s*([KkMmBb]?)$")


def parse_count(label: str) -> int:
    """Parse an aria-label like '12', '1.2K', '3M', '1,234' into an int.

    Unknown / empty labels return 0. This is deliberate: the scraper
    records 0 instead of skipping the card, because missing counts are
    common on freshly posted tweets.
    """
    if not label:
        return 0
    label = label.strip()
    m = _COUNT_RE.match(label)
    if m is None:
        return 0
    number_str, suffix = m.groups()
    number = float(number_str.replace(",", ""))
    multiplier = {
        "": 1, "K": 1_000, "k": 1_000,
        "M": 1_000_000, "m": 1_000_000,
        "B": 1_000_000_000, "b": 1_000_000_000,
    }[suffix]
    return int(number * multiplier)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_selectors.py -v`
Expected: 18 passed (2 url constant + 3 tweet_id + 8 parse_count + parametrized expansions).

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/_lib/selectors.py scripts/scrapers_x/tests/test_selectors.py
git commit -m "feat(scrapers_x): search URLs and DOM helpers"
```

---

## Task 7: Score function (TDD)

**Files:**
- Create: `scripts/scrapers_x/_lib/score.py`
- Test: `scripts/scrapers_x/tests/test_score.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/scrapers_x/tests/test_score.py
from _lib.score import score_topic, SCORE_THRESHOLD


def test_score_zero_when_no_interactions():
    assert score_topic(likes=0, replies=0, quotes=0, reposts=0) == 0


def test_score_weights():
    """replies weight 3, likes and quotes weight 2, reposts weight 1."""
    assert score_topic(likes=10, replies=0, quotes=0, reposts=0) == 20
    assert score_topic(likes=0, replies=10, quotes=0, reposts=0) == 30
    assert score_topic(likes=0, replies=0, quotes=10, reposts=0) == 20
    assert score_topic(likes=0, replies=0, quotes=0, reposts=10) == 10


def test_score_combined():
    """A 5/3/2/2 mix → 5*2 + 3*3 + 2*2 + 2*1 = 25."""
    assert score_topic(likes=5, replies=3, quotes=2, reposts=2) == 25


def test_threshold_default():
    """SCORE_THRESHOLD is 6 to filter single-engagement spam."""
    assert SCORE_THRESHOLD == 6
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_score.py -v`
Expected: `ModuleNotFoundError: No module named '_lib.score'`.

- [ ] **Step 3: Write the implementation**

```python
# scripts/scrapers_x/_lib/score.py
"""Pure scoring for X.com topic candidates.

Mirrors the SQL expression used in SKILL.md Step 2:

    (likes * 2) + (replies * 3) + (quotes * 2) + reposts

Reply weight is highest because comment threads on AI-monetization posts
tend to surface real numbers ("made $X from Y"). Like/quote weight 2 each.
Repost weight 1 to dampen viral-but-shallow posts.
"""

from __future__ import annotations

SCORE_THRESHOLD: int = 6


def score_topic(
    likes: int = 0,
    replies: int = 0,
    quotes: int = 0,
    reposts: int = 0,
) -> int:
    return likes * 2 + replies * 3 + quotes * 2 + reposts
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd <repo-root> && python -m pytest scripts/scrapers_x/tests/test_score.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/_lib/score.py scripts/scrapers_x/tests/test_score.py
git commit -m "feat(scrapers_x): score function"
```

---

## Task 8: CDP attach module

**Files:**
- Create: `scripts/scrapers_x/_lib/cdp.py`

(No tests in this task — CDP requires a live Chrome. Manual verification
in Task 9.)

- [ ] **Step 1: Write `cdp.py`**

```python
# scripts/scrapers_x/_lib/cdp.py
"""Chrome DevTools Protocol attach helpers for the X.com scraper.

We do NOT launch Chrome; the user keeps their own Chrome running with
``--remote-debugging-port=9228`` and the scraper attaches via
``playwright.chromium.connect_over_cdp``. Reusing the existing browser
is what inherits the X.com login session — we never see, store, or replay
cookies.

The two contracts enforced by this module:

1. Never tab-spam. We always reuse an existing x.com tab if one is open,
   and at most we will open ONE new tab in the user's browser.
2. Never block the user for long. Long waits use ``page.wait_for_timeout``
   with humane random delays.
"""

from __future__ import annotations

import contextlib
import logging
from typing import Iterator, Optional, Tuple

from playwright.sync_api import Browser, BrowserContext, Page

log = logging.getLogger("scrapers_x.cdp")

DEFAULT_CDP_URL = "http://localhost:9228"
X_HOST = "x.com"


class CDPError(RuntimeError):
    """Anything that goes wrong while attaching or picking a tab."""


def attach_chrome(cdp_url: str = DEFAULT_CDP_URL) -> Browser:
    try:
        from playwright.sync_api import sync_playwright as _sp
        p = _sp().__enter__()
    except Exception as e:
        raise CDPError(f"failed to start playwright: {e!r}") from e

    try:
        browser = p.chromium.connect_over_cdp(cdp_url)
    except Exception as e:
        with contextlib.suppress(Exception):
            p.stop()
        raise CDPError(
            f"cannot reach Chrome at {cdp_url}. "
            f"Relaunch Chrome with --remote-debugging-port=9228. Cause: {e!r}"
        ) from e

    browser._pw_handle = p  # type: ignore[attr-defined]
    log.info("attached to chrome at %s", cdp_url)
    return browser


def _stop(browser: Browser) -> None:
    pw = getattr(browser, "_pw_handle", None)
    if pw is not None:
        try:
            pw.stop()
        except Exception:
            pass


@contextlib.contextmanager
def scoped_chrome(cdp_url: str = DEFAULT_CDP_URL) -> Iterator[Browser]:
    browser = attach_chrome(cdp_url)
    try:
        yield browser
    finally:
        try:
            browser.close()
        except Exception:
            pass
        _stop(browser)


def _list_pages(browser: Browser) -> list[Page]:
    out: list[Page] = []
    for ctx in browser.contexts:
        out.extend(ctx.pages)
    return out


def find_x_page(browser: Browser) -> Optional[Page]:
    """The first open page whose URL contains x.com or twitter.com."""
    for page in _list_pages(browser):
        url = page.url or ""
        if X_HOST in url or "twitter.com" in url:
            return page
    return None


def open_or_reuse_x_page(
    browser: Browser, target_url: str
) -> Tuple[Page, bool]:
    existing = find_x_page(browser)
    if existing is not None:
        return existing, False

    contexts = browser.contexts
    if not contexts:
        raise CDPError(
            "Chrome has no default context. Close and relaunch Chrome with "
            "--remote-debugging-port=9228 --remote-allow-origins=*."
        )

    ctx: BrowserContext = contexts[0]
    page = ctx.new_page()
    page.goto(target_url, wait_until="domcontentloaded", timeout=30_000)
    return page, True


@contextlib.contextmanager
def x_page(
    target_url: str,
    cdp_url: str = DEFAULT_CDP_URL,
) -> Iterator[Tuple[Page, bool]]:
    with scoped_chrome(cdp_url) as browser:
        page, opened_new = open_or_reuse_x_page(browser, target_url)
        try:
            yield page, opened_new
        finally:
            if opened_new:
                with contextlib.suppress(Exception):
                    page.close()
```

- [ ] **Step 2: Manual smoke check (no automated test)**

Run:
```bash
python -c "import sys; sys.path.insert(0, 'scripts/scrapers_x'); from _lib.cdp import attach_chrome, find_x_page, scoped_chrome, x_page, DEFAULT_CDP_URL; print('cdp imports ok, DEFAULT_CDP_URL =', DEFAULT_CDP_URL)"
```

Expected: prints `cdp imports ok, DEFAULT_CDP_URL = http://localhost:9228`. No traceback.

- [ ] **Step 3: Commit**

```bash
git add scripts/scrapers_x/_lib/cdp.py
git commit -m "feat(scrapers_x): CDP attach helpers"
```

---

## Task 9: probe.py — manual health check

**Files:**
- Create: `scripts/scrapers_x/probe.py`

- [ ] **Step 1: Write probe.py**

```python
# scripts/scrapers_x/probe.py
"""One-shot health probe for the X.com scraper stack.

Run from the repo root:

    python scripts/scrapers_x/probe.py

What it does:
  1. Checks Chrome is reachable on :9228.
  2. Opens the 'top' search URL and prints the first 5 tweet URLs found.
  3. Exits.

This is a manual diagnostic. It does not write to SQLite.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _lib.cdp import scoped_chrome, find_x_page, open_or_reuse_x_page  # noqa: E402
from _lib.selectors import SEARCH_URLS, DOM_SELECTORS, parse_tweet_id  # noqa: E402


def main() -> int:
    url = SEARCH_URLS["top"]
    print(f"[probe] attaching to chrome...")
    with scoped_chrome() as browser:
        page, opened_new = open_or_reuse_x_page(browser, url)
        try:
            page.wait_for_selector(DOM_SELECTORS["tweet_root"], timeout=15_000)
            cards = page.query_selector_all(DOM_SELECTORS["tweet_root"])
            print(f"[probe] {len(cards)} tweet cards visible on first paint")
            for i, card in enumerate(cards[:5]):
                anchor = card.query_selector(DOM_SELECTORS["tweet_url"])
                if not anchor:
                    continue
                href = anchor.get_attribute("href") or ""
                full_url = href if href.startswith("http") else f"https://x.com{href}"
                tweet_id = parse_tweet_id(full_url)
                print(f"  [{i}] tweet_id={tweet_id}  url={full_url}")
        finally:
            if opened_new:
                try:
                    page.close()
                except Exception:
                    pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run probe against a live Chrome (manual)**

Pre-condition: a Chrome instance is running with
`--remote-debugging-port=9228` and the user is logged in to x.com.

Run:
```bash
cd <repo-root>
python scripts/scrapers_x/probe.py
```

Expected: prints `[probe] N tweet cards visible on first paint` followed by 5 lines of `tweet_id=...  url=...`. If 0 cards print, the selectors in `_lib/selectors.py` likely need an update — open x.com manually and inspect the DOM, then patch `DOM_SELECTORS`.

- [ ] **Step 3: Commit**

```bash
git add scripts/scrapers_x/probe.py
git commit -m "feat(scrapers_x): manual probe script"
```

---

## Task 10: crawl.py — main entry

**Files:**
- Create: `scripts/scrapers_x/crawl.py`

- [ ] **Step 1: Write crawl.py**

```python
# scripts/scrapers_x/crawl.py
"""X.com crawler for the twitter-x-daily-blog skill.

Run from the repo root:

    python scripts/scrapers_x/crawl.py --mode auto
    python scripts/scrapers_x/crawl.py --mode full --dry-run
    python scripts/scrapers_x/crawl.py --mode incremental --scroll-rounds 3

The script attaches to the user's Chrome on :9228, visits the search URLs
in selectors.SEARCH_URLS, scrolls each results page N times, extracts
tweet cards, and persists them to scripts/scrapers_x/data/x.sqlite3.
De-duplication is by URL UNIQUE constraint.
"""

from __future__ import annotations

import argparse
import logging
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _lib.cdp import scoped_chrome, open_or_reuse_x_page  # noqa: E402
from _lib.db import Database, TopicRow, utcnow_iso  # noqa: E402
from _lib.selectors import (  # noqa: E402
    DOM_SELECTORS,
    SEARCH_KEYWORD,
    SEARCH_URLS,
    parse_count,
    parse_tweet_id,
)

log = logging.getLogger("scrapers_x.crawl")
logging.basicConfig(level=logging.INFO, format="%(message)s")

DATA_DIR = HERE / "data"
DB_PATH = DATA_DIR / "x.sqlite3"


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="X.com scraper for AI monetization posts")
    p.add_argument("--mode", choices=["auto", "full", "incremental"], default="auto")
    p.add_argument("--scroll-rounds", type=int, default=5)
    p.add_argument("--humane-delay-ms", type=int, nargs=2, default=[800, 1400])
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def _extract_card(card, mode: str) -> TopicRow | None:
    """Extract a TopicRow from a tweet article element. Returns None on failure."""
    anchor = card.query_selector(DOM_SELECTORS["tweet_url"])
    if not anchor:
        return None
    href = anchor.get_attribute("href") or ""
    url = href if href.startswith("http") else f"https://x.com{href}"
    tweet_id = parse_tweet_id(url)
    if tweet_id is None:
        return None

    text_node = card.query_selector(DOM_SELECTORS["tweet_text"])
    body = (text_node.inner_text() if text_node else "").strip()
    if not body:
        return None

    user_node = card.query_selector(DOM_SELECTORS["user_name"])
    user_text = user_node.inner_text() if user_node else ""
    handle = None
    name = None
    if user_text:
        # "Display Name\n@handle" pattern
        lines = [s.strip() for s in user_text.split("\n") if s.strip()]
        if lines:
            name = lines[0]
        if len(lines) >= 2 and lines[1].startswith("@"):
            handle = lines[1][1:]

    def _count(testid: str) -> int:
        btn = card.query_selector(f'[data-testid="{testid}"]')
        if not btn:
            return 0
        # Walk up to the button ancestor for aria-label
        ancestor = btn.evaluate_handle(
            "el => el.closest('button') || el"
        )
        label = ancestor.get_attribute("aria-label") or ""
        return parse_count(label)

    now = utcnow_iso()
    return TopicRow(
        tweet_id=tweet_id,
        url=url,
        author_handle=handle,
        author_name=name,
        posted_at=None,  # X does not render a stable timestamp selector we can trust
        body_text=body,
        like_count=_count("like"),
        reply_count=_count("reply"),
        repost_count=_count("retweet"),
        quote_count=0,  # No stable selector; recorded as 0
        search_keyword=SEARCH_KEYWORD,
        search_mode=mode,
        first_seen_at=now,
        last_seen_at=now,
    )


def _scroll(page, rounds: int, delay_range: tuple[int, int]) -> None:
    for _ in range(rounds):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(random.randint(*delay_range))


def crawl(args: argparse.Namespace) -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = Database.open(DB_PATH)
    db.ensure_schema()
    run_id = db.record_run_start(mode=args.mode, started_at=utcnow_iso())

    items_seen = 0
    items_inserted = 0
    items_skipped = 0

    try:
        with scoped_chrome() as browser:
            for mode, url in SEARCH_URLS.items():
                log.info("[crawl] mode=%s url=%s", mode, url)
                page, opened_new = open_or_reuse_x_page(browser, url)
                try:
                    page.wait_for_selector(
                        DOM_SELECTORS["tweet_root"], timeout=15_000
                    )
                    _scroll(page, args.scroll_rounds, tuple(args.humane_delay_ms))
                    cards = page.query_selector_all(DOM_SELECTORS["tweet_root"])
                    items_seen += len(cards)
                    for card in cards:
                        row = _extract_card(card, mode)
                        if row is None:
                            items_skipped += 1
                            continue
                        if args.dry_run:
                            log.info("[dry-run] %s  likes=%s", row.url, row.like_count)
                            continue
                        before = db.topics.recent(within_seconds=86400 * 365 * 10)
                        db.topics.upsert(row)
                        after = db.topics.recent(within_seconds=86400 * 365 * 10)
                        if len(after) > len(before):
                            items_inserted += 1
                        else:
                            items_skipped += 1
                finally:
                    if opened_new:
                        try:
                            page.close()
                        except Exception:
                            pass
        db.record_run_end(
            run_id,
            finished_at=utcnow_iso(),
            status="ok",
            items_seen=items_seen,
            items_inserted=items_inserted,
            items_skipped=items_skipped,
        )
        log.info(
            "[crawl] done. seen=%d inserted=%d skipped=%d",
            items_seen, items_inserted, items_skipped,
        )
        return 0
    except Exception as e:
        log.error("[crawl] failed: %r", e)
        db.record_run_end(
            run_id,
            finished_at=utcnow_iso(),
            status="error",
            items_seen=items_seen,
            items_inserted=items_inserted,
            items_skipped=items_skipped,
        )
        return 1
    finally:
        db.close()


def main() -> int:
    args = _parse_args()
    return crawl(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Smoke-run in dry-run mode**

Pre-condition: Chrome on :9228 with x.com logged in.

Run:
```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode full --dry-run --scroll-rounds 2 --humane-delay-ms 600 1000
```

Expected output (abridged):
```
[crawl] mode=top url=https://x.com/search?...
[crawl] mode=live url=...
[dry-run] https://x.com/.../status/123... likes=N
...
[crawl] done. seen=K inserted=0 skipped=0
```

- [ ] **Step 3: Real run (writes to SQLite)**

```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode full --scroll-rounds 5 --humane-delay-ms 800 1400
```

Expected: exits 0, prints `inserted=N skipped=M`. Verify with:
```bash
python -c "import sqlite3; c=sqlite3.connect('scripts/scrapers_x/data/x.sqlite3'); print(list(c.execute('SELECT COUNT(*) FROM topics')))"
```
Expected: `[(N,)]` where N > 0.

- [ ] **Step 4: Re-run and confirm idempotency**

```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode full --scroll-rounds 5 --humane-delay-ms 800 1400
```

Expected: `inserted=0` or a small number (only newly visible tweets since the last run). The total row count in SQLite should not grow unboundedly.

- [ ] **Step 5: Commit**

```bash
git add scripts/scrapers_x/crawl.py
git commit -m "feat(scrapers_x): main crawl.py entry"
```

---

## Task 11: Final verification

**Files:** none (verification only)

- [ ] **Step 1: Run the entire test suite**

```bash
cd <repo-root>
python -m pytest scripts/scrapers_x/tests --cov=scripts/scrapers_x --cov-report=term-missing
```

Expected: all tests pass, line coverage ≥ 80% for `_lib/db.py`, `_lib/selectors.py`, `_lib/score.py`. CDP module and crawl.py are excluded from coverage (require live Chrome).

- [ ] **Step 2: Run ruff and mypy**

```bash
cd <repo-root>
ruff check scripts/scrapers_x/
mypy --strict scripts/scrapers_x/_lib/
```

Expected: zero errors. If ruff complains about `assert` in tests, add a `# noqa: S101` per-line, or configure `ruff` to allow asserts in `tests/`.

- [ ] **Step 3: Manual end-to-end smoke**

Pre-condition: Chrome on :9228, x.com logged in, `x.sqlite3` has rows from Task 10.

```bash
cd <repo-root>
python scripts/scrapers_x/crawl.py --mode auto --scroll-rounds 3
```

Expected: prints run summary, exits 0. Open the SKILL.md workflow steps in `.claude/skills/twitter-x-daily-blog/SKILL.md` and follow Step 2-6 manually to confirm a draft blog post is generated. Delete the draft after inspection (the skill does not commit).

- [ ] **Step 4: Final commit**

```bash
git status
```

If any untracked file in `scripts/scrapers_x/` is not ignored (e.g., a stray log), add a `.gitignore` line for it. Then:

```bash
git add scripts/scrapers_x/.gitignore 2>/dev/null || true
git commit --allow-empty -m "chore(scrapers_x): verify twitter-x-daily-blog end-to-end" || true
```

(Use `--allow-empty` only if there is nothing to commit; otherwise commit the actual diff.)

---

## Self-review

1. **Spec coverage**
   - §2 architecture → Tasks 1, 2
   - §3 data model → Tasks 4, 5
   - §4 crawl flow → Tasks 8, 9, 10
   - §5 candidate filter (SQL) → SKILL.md Step 2-4 + Task 7 score function
   - §6 draft generation → SKILL.md Step 5 (operator-driven, no code)
   - §7 error handling → Task 10's try/except + Task 4-5 error states
   - §8 testing → Task 11 + per-task pytest
   - §9 out of scope → enforced in Task 1 SKILL.md

2. **Placeholder scan**: no TBD / TODO / "implement later" / "add appropriate error handling".

3. **Type consistency**:
   - `Database.open(path)` defined in Task 4, used in Tasks 4, 5, 10.
   - `TopicRow` defined in Task 4, used in Tasks 4, 10.
   - `parse_tweet_id` / `parse_count` defined in Task 6, used in Tasks 9, 10.
   - `RunSummary` defined in Task 5, returned by `last_successful_run`.
   - `utcnow_iso` defined in Task 3, used in Tasks 3, 4, 5, 10.