from datetime import datetime, timezone

import pytest

from _lib.db import Database, TopicRow, utcnow_iso, now_minus_seconds_iso


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


@pytest.fixture
def db(tmp_path):
    """Fresh SQLite for each test."""
    path = tmp_path / "x.sqlite3"
    database = Database.open(path)
    database.ensure_schema()
    return database


def test_database_creates_schema(db, tmp_path):
    """Table topics exists after ensure_schema.

    NOTE: The 'runs' table is created in Task 5; this assertion intentionally
    only checks 'topics' so the test isolates Task 4's contract.
    """
    import sqlite3
    with sqlite3.connect(tmp_path / "x.sqlite3") as c:
        names = {row[0] for row in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert "topics" in names


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


# TODO(Task 5): Add test asserting the 'runs' table is created by ensure_schema.


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


def test_topics_exists(db):
    """exists() returns True iff tweet_id is already present."""
    row = TopicRow(
        tweet_id="42",
        url="https://x.com/x/status/42",
        author_handle="x", author_name="X", posted_at=None,
        body_text="hi", like_count=0, reply_count=0,
        repost_count=0, quote_count=0,
        search_keyword="AI变现", search_mode="top",
        first_seen_at="2026-07-02T00:00:00Z",
        last_seen_at="2026-07-02T00:00:00Z",
    )
    assert db.topics.exists("42") is False
    db.topics.upsert(row)
    assert db.topics.exists("42") is True
    assert db.topics.exists("999") is False