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

from _lib.cdp import scoped_chrome, open_or_reuse_x_page  # noqa: E402
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