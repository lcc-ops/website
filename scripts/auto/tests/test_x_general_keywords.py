"""Cross-module sync tests for the general-track x.com keyword table.

After scripts/scrapers_x/_lib/selectors.py was extended to one URL per
niche (vs. one fixed 'AI变现' URL), the prompt layer
(scripts/auto/_build_prompts.py) added a NICHE_SEARCH_KEYWORDS mirror so
the downstream `general` track can re-derive the niche from the
``search_keyword`` field stored on every x.com row.

These tests assert the two sides stay aligned. Pure unit tests — no DB,
no Chrome, no Claude call.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[3]
SCRIPTS_AUTO = REPO / "scripts" / "auto"
SCRAPERS_X = REPO / "scripts" / "scrapers_x" / "_lib"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"cannot load spec for {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_build = _load("_build_prompts_under_x_kw_test", SCRIPTS_AUTO / "_build_prompts.py")
_x_sel = _load("_x_selectors_under_test", SCRAPERS_X / "selectors.py")


def test_x_selectors_has_niche_to_query() -> None:
    """The x.com selectors module must expose NICHE_TO_QUERY (the new
    niche->query dict that replaces the single SEARCH_KEYWORD constant)."""
    assert hasattr(_x_sel, "NICHE_TO_QUERY"), (
        "scripts/scrapers_x/_lib/selectors.py must define NICHE_TO_QUERY"
    )
    assert isinstance(_x_sel.NICHE_TO_QUERY, dict)
    assert "ai" in _x_sel.NICHE_TO_QUERY, (
        "the legacy 'ai' niche must remain first so historical data shape is preserved"
    )


def test_niche_search_keywords_in_build_prompts() -> None:
    """The build-prompt module must mirror the x-side niche keys for the
    general track (minus the legacy 'ai' key, which only lives on the
    crawler side)."""
    assert hasattr(_build, "NICHE_SEARCH_KEYWORDS"), (
        "_build_prompts.py must expose NICHE_SEARCH_KEYWORDS so tests can "
        "verify the two sides agree"
    )
    x_keys = set(_x_sel.NICHE_TO_QUERY.keys()) - {"ai"}
    build_keys = set(_build.NICHE_SEARCH_KEYWORDS.keys())
    assert x_keys == build_keys, (
        f"x-side niche keys {x_keys} must match build-side niche keys "
        f"{build_keys}; otherwise the per-niche crawl supplies data the "
        f"downstream general track cannot categorize."
    )


def test_every_general_niche_has_a_category_mapping() -> None:
    """Every general niche exposed in NICHE_SEARCH_KEYWORDS must resolve
    via NICHE_TO_CATEGORY to one of the five legal frontmatter categories
    (payment / pricing / shipping / ops / ads). Otherwise the drafted
    post will be flagged as contaminated by _anti_ai_check.frontmatter_ok.
    """
    legal = {"payment", "pricing", "shipping", "ops", "ads"}
    bad: list[str] = []
    for niche in _build.NICHE_SEARCH_KEYWORDS:
        if niche not in _build.NICHE_TO_CATEGORY:
            bad.append(f"{niche}: no NICHE_TO_CATEGORY entry")
            continue
        if _build.NICHE_TO_CATEGORY[niche] not in legal:
            bad.append(f"{niche} -> {_build.NICHE_TO_CATEGORY[niche]} (not in {legal})")
    assert not bad, f"unmapped or illegal category: {bad}"


def test_niche_search_keywords_not_all_ai_terms() -> None:
    """The x-side queries must not trip the AI-keyword blocklist; otherwise
    the general-track filter (which drops posts whose body contains any
    AI_KEYWORDS) would silently drop legitimate non-AI posts whose
    crawled query string happens to mention e.g. 'Agent'."""
    ai_lower = {k.lower() for k in _build.AI_KEYWORDS}
    bad: list[str] = []
    for niche, query in _build.NICHE_SEARCH_KEYWORDS.items():
        if query.lower() in ai_lower:
            bad.append(f"{niche}: '{query}' matches AI_KEYWORDS")
    assert not bad, f"general-track x queries collide with AI_KEYWORDS: {bad}"


def test_x_search_urls_cover_every_niche_x_mode_pair() -> None:
    """For each niche, SEARCH_URLS must produce a (niche, mode) entry for
    both 'top' and 'live' modes. A missing entry means the crawler skips
    that combination silently."""
    for niche in _x_sel.NICHE_TO_QUERY:
        for mode in ("top", "live"):
            assert (niche, mode) in _x_sel.SEARCH_URLS, (
                f"SEARCH_URLS missing (niche={niche}, mode={mode})"
            )


def test_x_search_urls_are_well_formed() -> None:
    """Every URL must point at x.com/search?q=...&src=typed_query and carry
    a non-empty query. Catches accidental URL template drift."""
    for (niche, mode), url in _x_sel.SEARCH_URLS.items():
        assert url.startswith("https://x.com/search?q="), f"{niche}/{mode}: {url}"
        assert "src=typed_query" in url, f"{niche}/{mode}: missing src=typed_query"
        assert mode not in url or f"f={mode}" in url, (
            f"{niche}/{mode}: live mode without f=live"
        )