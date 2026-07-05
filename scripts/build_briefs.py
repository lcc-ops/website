#!/usr/bin/env python3
"""Regenerate the zsxq briefs index from SQLite.

Companion script for the zsxq-daily-blog skill. Reads topics from
`scripts/scrapers/data/zsxq.sqlite3`, filters to AI-related posts from
the last 24 hours, ranks by interaction score, and writes a Markdown
briefs file ready for review / drafting.

Mirrors the inline query that the skill's working procedure step 5
says to run otherwise; moves it into a single re-runnable command so
operators do not have to answer Bash permission prompts for repeated
inline `python -c "..."` calls.

Usage:
    python scripts/build_briefs.py [--since-hours 24] [--top 10] [--out <path>]
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "scripts" / "scrapers" / "data" / "zsxq.sqlite3"
DEFAULT_OUT = ROOT / "scripts" / "scrapers" / "data" / "briefs.md"

# Same token list as references/keyword_list.md. Kept in code so the
# script runs without depending on the skill's references/ tree.
AI_KEYWORDS = [
    r"AI", r"GPT", r"ChatGPT", r"Claude", r"LLM",
    r"大模型", r"模型", r"agent", r"智能体",
    r"prompt", r"提示词", r"RAG", r"知识库",
    r"Seedance", r"Sora", r"Kling",
    r"Midjourney", r"Stable\s*Diffusion",
    r"Gemini", r"Claude\s*Code", r"Cursor", r"codex", r"Copilot",
    r"ComfyUI", r"lora", r"fine-?tune", r"Embedding", r"向量",
]
KW_RE = re.compile("|".join(AI_KEYWORDS), re.IGNORECASE)


def has_ai_keyword(text: str) -> bool:
    return bool(text) and bool(KW_RE.search(text))


def query_candidates(conn: sqlite3.Connection, since_hours: int, lookahead: int) -> list:
    """Pull fresh topics; rank by engagement; filter to AI in Python."""
    sql = """
        SELECT
            topic_id, group_id, group_name, author, posted_at,
            title, body_text, source_url,
            like_count, comment_count, readers_count,
            (coalesce(like_count, 0) * 2
             + coalesce(comment_count, 0) * 3) AS score
        FROM topics
        WHERE last_seen_at >= datetime('now', ?)
          AND last_seen_at != first_seen_at
          AND body_text IS NOT NULL
        ORDER BY score DESC, posted_at DESC
        LIMIT ?
    """
    return list(conn.execute(sql, (f"-{since_hours} hours", lookahead)))


def render_briefs(rows: list[sqlite3.Row], top: int, since_hours: int) -> tuple[str, int]:
    """Build the briefs index. AI-filter, then cap to top N."""
    kept: list[sqlite3.Row] = []
    skipped_non_ai = 0
    for row in rows:
        if not has_ai_keyword(row["body_text"] or ""):
            skipped_non_ai += 1
            continue
        kept.append(row)
        if len(kept) >= top:
            break

    lines = [
        "# zsxq briefs",
        "",
        f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_  ",
        f"_Window: last {since_hours}h · AI-filter applied · capped at top {top}_",
        "",
        "| # | Topic | Score | Likes | Comments | Preview |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for i, row in enumerate(kept, start=1):
        prev = (row["body_text"] or "").replace("\n", " ")[:160]
        lines.append(
            f"| {i} | `{row['topic_id']}` "
            f"| {row['score']} "
            f"| {row['like_count'] or 0} "
            f"| {row['comment_count'] or 0} "
            f"| {prev} |"
        )

    if not kept:
        lines.append("| — | _no AI-related candidates in window_ | — | — | — | — |")

    lines.extend([
        "",
        "## Notes",
        "",
        f"- Considered {len(rows)} fresh topic(s); kept {len(kept)} after AI filter.",
        f"- Dropped {skipped_non_ai} topic(s) without an AI keyword match.",
        "- Score formula: `(likes * 2) + (comments * 3)`. Tiebreaker: `posted_at DESC`.",
        "",
    ])
    return "\n".join(lines), len(kept)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since-hours", type=int, default=24,
                        help="Lookback window in hours (default: 24)")
    parser.add_argument("--top", type=int, default=10,
                        help="Maximum number of briefs to keep (default: 10)")
    parser.add_argument("--lookahead", type=int, default=30,
                        help="Rows pulled before AI filter + top cap (default: 30)")
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB),
                        help="Path to zsxq.sqlite3")
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT),
                        help="Path to briefs.md")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"[err] SQLite not found at {db_path}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = query_candidates(conn, args.since_hours, args.lookahead)
    finally:
        conn.close()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    md, kept = render_briefs(rows, args.top, args.since_hours)
    out_path.write_text(md, encoding="utf-8")

    print(f"[ok] {out_path.relative_to(ROOT)} — {kept} brief(s); "
          f"considered {len(rows)}; window {args.since_hours}h.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
