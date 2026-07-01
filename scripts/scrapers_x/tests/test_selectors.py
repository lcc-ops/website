import pytest

from _lib.selectors import (
    SEARCH_URLS,
    parse_tweet_id,
    parse_count,
)


def test_search_urls_contains_top_and_live():
    assert "top" in SEARCH_URLS
    assert "live" in SEARCH_URLS
    assert "AI%E5%8F%98%E7%8E%B0" in SEARCH_URLS["top"]
    assert "f=live" in SEARCH_URLS["live"]


@pytest.mark.parametrize("url,expected", [
    ("https://x.com/foo/status/1234567890", "1234567890"),
    ("https://twitter.com/bar/status/42", "42"),
    ("https://x.com/baz/status/999999999999999999", "999999999999999999"),
])
def test_parse_tweet_id(url, expected):
    assert parse_tweet_id(url) == expected


def test_parse_tweet_id_invalid():
    assert parse_tweet_id("https://example.com/foo") is None
    assert parse_tweet_id("not a url") is None


@pytest.mark.parametrize("label,expected", [
    ("12", 12),
    ("1.2K", 1200),
    ("12K", 12000),
    ("1.5M", 1_500_000),
    ("2.3B", 2_300_000_000),
    ("1,234", 1234),
    ("Like", 0),  # unknown -> 0
    ("", 0),
])
def test_parse_count(label, expected):
    assert parse_count(label) == expected
