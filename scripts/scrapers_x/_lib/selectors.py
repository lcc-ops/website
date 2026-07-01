"""Constants and DOM helpers for the X.com scraper.

The two contracts:

1. SEARCH_URLS - the two search result pages the crawler visits. Change
   the keyword here, not in crawl.py.

2. parse_tweet_id / parse_count - pure functions for extracting fields
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
