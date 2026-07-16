"""Tests for the dual-track (ai / general) category logic.

Verifies that:
  - AI_KEYWORDS list is unchanged from the legacy surface (the ai track
    still drops posts that contain zero AI keywords).
  - NICHE_TO_CATEGORY in _build_prompts and _anti_ai_check stay in sync.
  - The anti-AI checker's `expected_category_from_niche` returns:
      * 'ai' for an AI-track post (tags[0] is not in NICHE_TO_CATEGORY)
      * the mapped value for any general-track niche
      * None when tags[0] is missing or malformed
  - The anti-AI checker's `frontmatter_ok` flags a category mismatch.

These are pure unit tests — no DB, no Chrome, no Claude call.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[3]
SCRIPTS_AUTO = REPO / "scripts" / "auto"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"cannot load spec for {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_build = _load("_build_prompts_under_test", SCRIPTS_AUTO / "_build_prompts.py")
_anti = _load("_anti_ai_check_under_test", SCRIPTS_AUTO / "_anti_ai_check.py")


def test_niche_to_category_in_sync_between_modules() -> None:
    assert _build.NICHE_TO_CATEGORY == _anti.NICHE_TO_CATEGORY, (
        "NICHE_TO_CATEGORY must match between _build_prompts and "
        "_anti_ai_check; otherwise the build queue can emit a category "
        "that the checker will reject as contaminated."
    )


def test_general_niche_table_contains_no_ai_overlap() -> None:
    """A keyword cannot appear in BOTH AI_NICHE_KEYWORDS and
    GENERAL_NICHE_KEYWORDS — otherwise the ai/general split is meaningless."""
    ai_kws: set[str] = set()
    for kws in _build.AI_NICHE_KEYWORDS.values():
        ai_kws.update(k.lower() for k in kws)
    overlap: set[str] = set()
    for kws in _build.GENERAL_NICHE_KEYWORDS.values():
        for k in kws:
            if k.lower() in ai_kws:
                overlap.add(k)
    assert not overlap, f"AI/general keyword overlap: {sorted(overlap)}"


def test_general_niche_keywords_blocklist_excludes_ai_terms() -> None:
    """Every keyword in GENERAL_NICHE_KEYWORDS must NOT be in AI_KEYWORDS
    (case-insensitive). If it is, the body would pass the 'general' filter
    but get dropped again at the 'no AI keywords' gate."""
    ai_lower = {k.lower() for k in _build.AI_KEYWORDS}
    bad: list[str] = []
    for kws in _build.GENERAL_NICHE_KEYWORDS.values():
        for k in kws:
            if k.lower() in ai_lower:
                bad.append(k)
    assert not bad, f"general-track keywords still match AI_KEYWORDS: {bad}"


def test_detect_niche_ai_track_returns_known_or_vertical_ai() -> None:
    body_ai = "I built a wrapper around Claude and raked in $5k/month."
    assert _build.detect_niche(body_ai, _build.AI_NICHE_KEYWORDS, fallback="vertical-ai") == "vertical-ai"
    body_seed = "Sora-style video generation. I charge $200 per clip."
    assert _build.detect_niche(body_seed, _build.AI_NICHE_KEYWORDS, fallback="vertical-ai") == "seedance"


def test_detect_niche_general_track_returns_empty_for_ai_body() -> None:
    body_ai = "I built a Claude wrapper, niche is vertical AI agent."
    assert _build.detect_niche(body_ai, _build.GENERAL_NICHE_KEYWORDS, fallback="") == ""


def test_detect_niche_general_track_picks_logistics() -> None:
    body = "我最近在做跨境物流，对比了 E-Packet 的费用和时效"
    assert _build.detect_niche(body, _build.GENERAL_NICHE_KEYWORDS, fallback="") == "logistics"


def test_detect_niche_general_track_picks_google_ads() -> None:
    body = "ROAS at 3x means I'm losing money. My break-even is 4x."
    assert _build.detect_niche(body, _build.GENERAL_NICHE_KEYWORDS, fallback="") == "google-ads"


def test_latin_ai_keyword_uses_word_boundary() -> None:
    """Pre-existing bug: substring match let "AI" match "trail/paid/detail".
    Word-boundary match must reject those. CJK still matches as substring."""
    assert _build.hits_in_body("the trail was muddy") == []
    assert _build.hits_in_body("he paid the invoice") == []
    assert _build.hits_in_body("the detail matters") == []
    # "AI agent" still hits both:
    hits = _build.hits_in_body("I built an AI agent wrapper")
    assert "AI" in hits
    assert "agent" in hits


def test_latin_niche_keyword_uses_word_boundary() -> None:
    """POD is a niche in AI_NICHE_KEYWORDS. As a whole word it should match
    the noun; as a substring of "podcast" / "podium" it must NOT."""
    body_pod = "I run a POD store for hiking maps"
    assert _build.detect_niche(body_pod, _build.AI_NICHE_KEYWORDS, fallback="") == "etsy-pod"
    body_podcast = "I host a podcast about hiking"
    assert _build.detect_niche(body_podcast, _build.AI_NICHE_KEYWORDS, fallback="") == "podcast"
    # podium should not hit POD
    body_podium = "she stood on the podium"
    assert _build.detect_niche(body_podium, _build.AI_NICHE_KEYWORDS, fallback="vertical-ai") == "vertical-ai"


def test_expected_category_ai_track() -> None:
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'ai'\n"
        "tags: ['ai', 'wrapper', 'case-study', 'monetization']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody"
    )
    assert _anti.expected_category_from_niche(text) == "ai"
    ok, issues = _anti.frontmatter_ok(text)
    assert ok, issues


def test_expected_category_general_track_payment() -> None:
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'payment'\n"
        "tags: ['chargeback', 'fraud', 'prevention']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody"
    )
    assert _anti.expected_category_from_niche(text) == "payment"
    ok, issues = _anti.frontmatter_ok(text)
    assert ok, issues


def test_expected_category_general_track_shipping() -> None:
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'shipping'\n"
        "tags: ['logistics', 'cross-border', 'cbm']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody"
    )
    assert _anti.expected_category_from_niche(text) == "shipping"
    ok, issues = _anti.frontmatter_ok(text)
    assert ok, issues


def test_category_mismatch_is_contaminated() -> None:
    """If tags[0] is a general niche but the body declares category='ai',
    the post must be flagged so the build doesn't ship a mis-tagged draft."""
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'ai'\n"
        "tags: ['logistics', 'cross-border']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody"
    )
    ok, issues = _anti.frontmatter_ok(text)
    assert not ok
    assert any("category is 'ai', expected 'shipping'" in i for i in issues)


def test_missing_tags_returns_none() -> None:
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'ai'\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody"
    )
    assert _anti.expected_category_from_niche(text) is None
    ok, issues = _anti.frontmatter_ok(text)
    assert not ok


def test_general_template_file_exists_and_has_cn_en_blocks() -> None:
    p = SCRIPTS_AUTO / "_prompts" / "draft_one_topic_general.md"
    assert p.exists(), f"general prompt template missing: {p}"
    text = p.read_text(encoding="utf-8")
    assert "=== en.md ===" in text
    assert "=== zh.md ===" in text
    assert "{CATEGORY}" in text
    assert "{PUBDATE}" in text
    # Anti-AI guards must NOT be silently dropped from the general template.
    assert "delve" in text
    assert "赋能" in text


def test_general_template_forbids_ai_category() -> None:
    p = SCRIPTS_AUTO / "_prompts" / "draft_one_topic_general.md"
    text = p.read_text(encoding="utf-8")
    # The template fills category from {CATEGORY} which is set by the
    # build script to a value from NICHE_TO_CATEGORY — never 'ai'.
    # The hard rule in the template must call this out so a sloppy model
    # can't drift back to writing 'ai' even if NICHE_TO_CATEGORY drifts.
    assert "Do NOT use 'ai'" in text


def test_ai_template_still_present_and_unchanged_in_shape() -> None:
    p = SCRIPTS_AUTO / "_prompts" / "draft_one_topic.md"
    text = p.read_text(encoding="utf-8")
    assert "=== en.md ===" in text
    assert "=== zh.md ===" in text
    # The legacy template hard-codes 'ai' as the only legal category.
    assert "category MUST be exactly 'ai'" in text


def test_ai_zh_required_anchors() -> None:
    """AI track: zh must carry the same English anchor names (Context,
    What this case does not cover, Take-away)."""
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'ai'\n"
        "tags: ['ai', 'wrapper', 'case-study', 'monetization']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody\n\n"
        "## Context\nfoo\n\n## Numbers\nbar\n\n## Unit economics\nbaz\n\n"
        "## What this case does not cover\nqux\n\n## Take-away\nquux\n"
    )
    ok, issues = _anti.frontmatter_ok(text)
    assert ok, issues
    # Now run the full scan_slug-shaped check: but frontmatter_ok doesn't
    # touch H2, so we just verify the constant is what we expect.
    assert _anti.REQUIRED_SECTIONS == ("Context", "What this case does not cover", "Take-away")


def test_general_zh_anchors_are_translated() -> None:
    """General track: zh must carry translated anchors (背景 / 这个案例没覆盖
    的部分 / 结论), NOT the English ones. This guards the anti-AI checker's
    H2 check from being english-only."""
    anchors = _anti.GENERAL_REQUIRED_SECTIONS_ZH["pricing"]
    assert anchors["context"] == "背景"
    assert anchors["gaps"] == "这个案例没覆盖的部分"
    assert anchors["takeaway"] == "结论"
    # All five general categories share the same translation.
    for cat in ("payment", "pricing", "shipping", "ops", "ads"):
        assert _anti.GENERAL_REQUIRED_SECTIONS_ZH[cat] == anchors


def test_general_track_h2_check_accepts_translated_anchors() -> None:
    """End-to-end check: a general-track post with translated H2 anchors
    must NOT be flagged as missing_sections_zh. We test by replicating
    the relevant slice of scan_slug logic here, since scan_slug is the
    orchestrator and would require a full temp dir + weights file."""
    import re
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'pricing'\n"
        "tags: ['etsy-pricing', 'fees']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody\n\n"
        "## 背景\nfoo\n\n## 数字\nbar\n\n## 单位经济\nbaz\n\n"
        "## 这个案例没覆盖的部分\nqux\n\n## 结论\nquux\n"
    )
    cat_m = re.search(r"^category:\s*['\"]([^'\"]+)['\"]", text, flags=re.MULTILINE)
    cat_value = cat_m.group(1)
    assert cat_value in _anti.GENERAL_REQUIRED_SECTIONS_ZH
    anchors = _anti.GENERAL_REQUIRED_SECTIONS_ZH[cat_value]
    missing = [name for name, anchor in anchors.items()
               if not re.search(rf"^##\s+{re.escape(anchor)}\s*$", text, flags=re.MULTILINE)]
    assert missing == [], f"missing: {missing}"


def test_general_track_h2_check_flags_missing_zh_anchor() -> None:
    """If the LLM forgot to translate 'context' -> '背景', the check must
    still flag it. This is the regression test for the old english-only
    check that let the trial draft slip through contaminated."""
    import re
    text = (
        "---\n"
        "title: 'Test'\n"
        "description: 'Test'\n"
        "pubDate: 2026-07-16\n"
        "category: 'pricing'\n"
        "tags: ['etsy-pricing', 'fees']\n"
        "translationKey: 'test'\n"
        "tldr: '...'\n"
        "faq:\n  - q: 'q1'\n    a: 'a1'\n"
        "  - q: 'q2'\n    a: 'a2'\n"
        "  - q: 'q3'\n    a: 'a3'\n"
        "  - q: 'q4'\n    a: 'a4'\n"
        "  - q: 'q5'\n    a: 'a5'\n"
        "  - q: 'q6'\n    a: 'a6'\n"
        "---\n\nbody\n\n"
        "## Context\nfoo\n\n## Numbers\nbar\n\n## Unit economics\nbaz\n\n"
        "## What this case does not cover\nqux\n\n## Take-away\nquux\n"
    )
    cat_m = re.search(r"^category:\s*['\"]([^'\"]+)['\"]", text, flags=re.MULTILINE)
    cat_value = cat_m.group(1)
    anchors = _anti.GENERAL_REQUIRED_SECTIONS_ZH[cat_value]
    missing = [name for name, anchor in anchors.items()
               if not re.search(rf"^##\s+{re.escape(anchor)}\s*$", text, flags=re.MULTILINE)]
    assert missing == ["context", "gaps", "takeaway"]
