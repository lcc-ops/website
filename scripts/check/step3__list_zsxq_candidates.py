"""List zsxq candidate topics from the last 24h, written to a UTF-8 file (terminal may not render CJK).

Run: python scripts/check/step3__list_zsxq_candidates.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DB = REPO / "scripts" / "scrapers" / "data" / "zsxq.sqlite3"
OUT = REPO / "scripts" / "check" / "_out_zsxq_candidates.txt"


def main() -> int:
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT topic_id, posted_at, author, like_count, comment_count, body_text
        FROM topics
        WHERE last_seen_at >= datetime('now', '-1 day')
          AND body_text IS NOT NULL
        ORDER BY (coalesce(like_count, 0) * 2 + comment_count * 3) DESC
        LIMIT 30
        """
    ).fetchall()
    out_lines: list[str] = []
    for r in rows:
        score = (r["like_count"] or 0) * 2 + (r["comment_count"] or 0) * 3
        out_lines.append(
            f"[score={score} | L={r['like_count']} C={r['comment_count']}] "
            f"{r['posted_at']}  topic_id={r['topic_id']}"
        )
        out_lines.append(f"  author={r['author']}")
        out_lines.append(f"  body={r['body_text']}")
        out_lines.append("")
    OUT.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
