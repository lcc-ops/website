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
# Search keywords. Each entry maps a niche tag (matching
# scripts/auto/_build_prompts.NICHE_TO_CATEGORY) to the literal x.com
# query string the crawler will issue. The first entry remains the legacy
# AI monetization query so the historic data shape is preserved.
#
# To add a new niche, append to NICHE_TO_QUERY (and the matching body-side
# keywords in scripts/auto/_build_prompts.GENERAL_NICHE_KEYWORDS so the
# downstream `general` track can re-derive the niche).
# ---------------------------------------------------------------------------
from urllib.parse import quote

# Niche tag (matches _build_prompts.NICHE_TO_CATEGORY keys) -> x.com query.
# Each query is the **bare tag word** as it appears in src/content/blog
# frontmatter (tags[0]). x.com search tolerates these as-is; wider
# composite phrases (e.g. "PayPal 手续费" instead of "paypal") were tried
# and produced sparse results. Keep the legacy "AI变现" first so the
# historical data shape is preserved.
NICHE_TO_QUERY: dict[str, str] = {
    "ai":               "AI变现",
    "logistics":        "E邮宝 小包 跨境物流",
    "cbm":              "CBM 抛货 体积重",
    "payment-fees":     "PayPal 手续费",
    "chargeback":       "拒付 拒赔 撤单",
    "etsy-pricing":     "Etsy 佣金 费用",
    "amazon-pricing":   "FBA 仓储费 亚马逊",
    "dropshipping-costs": "一件代发 Dropshipping",
    "google-ads":       "Google 广告 投产比",
    "freelance-pricing": "自由职业 时薪 定价",
    "lead-gen":         "B2B 销售线索 中介",
    "podcast-monetize": "播客 变现 广告",
    "youtube-creator":  "YouTube CPM 收益",
    "shopify-pricing":  "Shopify 订阅 费用",
}


def _build_url(query: str, mode: str) -> str:
    enc = quote(query)
    base = f"https://x.com/search?q={enc}&src=typed_query"
    return f"{base}&f=live" if mode == "live" else base


# { (niche, mode): url } — derived from NICHE_TO_QUERY above. Modes are
# "top" (default ranking) and "live" (chronological).
SEARCH_URLS: dict[tuple[str, str], str] = {
    (niche, mode): _build_url(query, mode)
    for niche, query in NICHE_TO_QUERY.items()
    for mode in ("top", "live")
}


# Back-compat: keep SEARCH_KEYWORD as the *first* niche's query so callers
# that still import the legacy single-value symbol keep working.
SEARCH_KEYWORD: str = next(iter(NICHE_TO_QUERY.values()))

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


_COUNT_RE = re.compile(r"^\s*([\d,.]+)\s*([KkMmBb]?)")


def parse_count(label: str) -> int:
    """Parse the leading number out of an aria-label.

    X.com renders the interaction count as the FIRST token in the button's
    aria-label, followed by a localized verb (e.g. ``"25 ϲ��������ϲ��"`` for
    Likes, ``"1.2K �ظ�"`` for Replies, ``"3M ��ת"`` for Reposts). Earlier
    scrapers assumed the whole string was the count, which silently yielded
    0 once X started localizing the verb.

    Returns the parsed integer; 0 if the leading token is missing or
    unparseable. Missing counts are common on freshly posted tweets and
    are recorded as 0 rather than skipping the card.
    """
    if not label:
        return 0
    label = label.strip()
    m = _COUNT_RE.match(label)
    if m is None:
        return 0
    number_str, suffix = m.groups()
    try:
        number = float(number_str.replace(",", ""))
    except ValueError:
        return 0
    multiplier = {
        "": 1, "K": 1_000, "k": 1_000,
        "M": 1_000_000, "m": 1_000_000,
        "B": 1_000_000_000, "b": 1_000_000_000,
    }[suffix]
    return int(number * multiplier)
