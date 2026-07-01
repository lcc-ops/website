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
    handle: str | None = None
    name: str | None = None
    if user_text:
        # "Display Name\n@handle" pattern
        lines = [s.strip() for s in user_text.split("\n") if s.strip()]
        if lines:
            name = lines[0]
        if len(lines) >= 2 and lines[1].startswith("@"):
            handle = lines[1][1:]

    def _count(testid: str) -> int:
        # X renders like/reply/retweet icons inside the testid element,
        # and the count is on the testid element itself's aria-label
        # (the parent button is unlabeled on X.com).
        node = card.query_selector(f'[data-testid="{testid}"]')
        if not node:
            return 0
        label = node.get_attribute("aria-label") or ""
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
                            log.info(
                                "[dry-run] %s  likes=%d replies=%d",
                                row.url, row.like_count, row.reply_count,
                            )
                            continue
                        existed = db.topics.exists(row.tweet_id)
                        db.topics.upsert(row)
                        if existed:
                            items_skipped += 1
                        else:
                            items_inserted += 1
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