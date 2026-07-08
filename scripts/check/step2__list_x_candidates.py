"""List x.com candidate tweets from the last 24h, written to a UTF-8 file.

Run: python scripts/check/step2__list_x_candidates.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "scripts" / "scrapers_x" / "data" / "x.sqlite3"
OUT = REPO / "scripts" / "check" / "_out_x_candidates.txt"


def main() -> int:
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT tweet_id, posted_at, author_handle,
               like_count, reply_count, repost_count, quote_count, body_text
        FROM topics
        WHERE last_seen_at >= datetime('now', '-1 day')
          AND last_seen_at != first_seen_at
          AND body_text IS NOT NULL
        ORDER BY (coalesce(like_count, 0) * 2
                  + coalesce(reply_count, 0) * 3
                  + coalesce(quote_count, 0) * 2
                  + coalesce(repost_count, 0)) DESC
        LIMIT 30
        """
    ).fetchall()
    out_lines: list[str] = []
    for r in rows:
        score = (
            (r["like_count"] or 0) * 2
            + (r["reply_count"] or 0) * 3
            + (r["quote_count"] or 0) * 2
            + (r["repost_count"] or 0)
        )
        out_lines.append(
            f"[score={score} | L={r['like_count']} R={r['reply_count']} "
            f"Q={r['quote_count']} RT={r['repost_count']}] "
            f"@{r['author_handle']} {r['posted_at']}  tweet_id={r['tweet_id']}"
        )
        out_lines.append(r["body_text"])
        out_lines.append("---")
    OUT.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
