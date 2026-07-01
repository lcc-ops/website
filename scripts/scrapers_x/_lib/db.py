"""SQLite persistence for the X.com scraper.

Public surface (grows across later tasks):

    db = Database.open(path)
    db.ensure_schema()
    run_id = db.record_run_start(mode='full', started_at=...)
    db.record_run_end(run_id, status='ok', items_seen=..., ...)
    if db.topics.exists(tweet_id): ...
    db.topics.upsert(topic_row)   # URL UNIQUE → INSERT OR IGNORE
    db.topics.touch_last_seen(tweet_id, last_seen_at_iso)

Design choices mirror scripts/scrapers/_lib/db.py:
- All timestamps are ISO-8601 UTC strings ending in 'Z'.
- Every SQL uses '?' placeholders. No f-string SQL.
- Foreign keys are enabled.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


def utcnow_iso() -> str:
    """ISO-8601 UTC string with second precision and trailing Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_minus_seconds_iso(seconds: int) -> str:
    """ISO-8601 UTC string for ``seconds`` ago."""
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

    def last_successful_run(self) -> Optional[RunSummary]:
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

    def close(self) -> None:
        self._c.close()
