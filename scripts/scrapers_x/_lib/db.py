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