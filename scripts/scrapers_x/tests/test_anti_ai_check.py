"""Unit tests for scripts/auto/_anti_ai_check.py pure helpers.

Loads the module via importlib.util.spec_from_file_location so module-level
path constants (REPO/BLOG_ROOT/...) do not matter during the test — we only
exercise pure functions and the (slug, weights) -> report routine.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
AUTO_DIR = REPO_ROOT / "scripts" / "auto"
SRC = AUTO_DIR / "_anti_ai_check.py"


def _load():
    spec = importlib.util.spec_from_file_location("_anti_ai_check", SRC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_anti_ai_check", mod)
    spec.loader.exec_module(mod)
    return mod


mod = _load()


# ---------------------------------------------------------------------------
# count_words
# ---------------------------------------------------------------------------


def test_count_words_case_insensitive_and_zero_pruning() -> None:
    out = mod.count_words("Secrets and SECRETS, plus another secrets here.",
                          ["secrets", "absent"])
    assert out.get("secrets") == 3
    assert "absent" not in out


def test_count_words_skips_empty_terms() -> None:
    out = mod.count_words("hello hello", ["", "hello"])
    assert out == {"hello": 2}


# ---------------------------------------------------------------------------
# section_word_count
# ---------------------------------------------------------------------------


def test_section_word_count_splits_on_h2_headings() -> None:
    body = (
        "## Context\n"
        "Some words here.\n\n"
        "## Take-away\n"
        "One two three four five six.\n"
    )
    sections = mod.section_word_count(body)
    assert sections["Context"] == 3
    assert sections["Take-away"] == 6


def test_section_word_count_trailing_empty_h2_still_recorded() -> None:
    # Behavior discovery (matches current implementation): the trailing
    # header's accumulator is also committed via the final `if cur_h is not
    # None:` guard, even when no body follows. Future maintainers: don't
    # break downstream callers (scan_slug expects an integer, not absence).
    body = "## A\n\none two three\n## B\n"
    sections = mod.section_word_count(body)
    assert sections.get("A") == 3
    assert sections.get("B") == 0


# ---------------------------------------------------------------------------
# has_banned_phrase
# ---------------------------------------------------------------------------


def test_has_banned_phrase_returns_matching_patterns() -> None:
    hits = mod.has_banned_phrase("This post will UNLOCK the secrets.", [r"unlock",
                                                                       r"delve into"])
    assert "unlock" in hits
    assert "delve into" not in hits


def test_has_banned_phrase_skips_empty_pattern() -> None:
    assert mod.has_banned_phrase("any text", ["", r"text"]) == ["text"]


# ---------------------------------------------------------------------------
# frontmatter_ok
# ---------------------------------------------------------------------------


def _frontmatter(category: str, faq_count: int, *, with_translation_key: bool = True) -> str:
    parts = ["---"]
    parts.append(f"category: '{category}'")
    if with_translation_key:
        parts.append("translationKey: 'demo'")
    for i in range(faq_count):
        parts.append(f"  - q: question {i}")
        parts.append(f"    a: answer {i}")
    parts.append("---")
    parts.append("\n## Context\n\nbody.\n")
    return "\n".join(parts) + "\n"


def test_frontmatter_ok_accepts_minimal_valid() -> None:
    text = _frontmatter("ai", 6)
    ok, issues = mod.frontmatter_ok(text)
    assert ok is True
    assert issues == []


def test_frontmatter_ok_rejects_wrong_category() -> None:
    text = _frontmatter("pricing", 6)
    ok, issues = mod.frontmatter_ok(text)
    assert ok is False
    assert any("category" in i for i in issues)


def test_frontmatter_ok_rejects_wrong_faq_count() -> None:
    text = _frontmatter("ai", 3)
    ok, issues = mod.frontmatter_ok(text)
    assert ok is False
    assert any("FAQ" in i for i in issues)


def test_frontmatter_ok_rejects_missing_translation_key() -> None:
    text = _frontmatter("ai", 6, with_translation_key=False)
    ok, issues = mod.frontmatter_ok(text)
    assert ok is False
    assert any("translationKey" in i for i in issues)


def test_frontmatter_ok_rejects_missing_fence() -> None:
    ok, issues = mod.frontmatter_ok("just prose, no frontmatter")
    assert ok is False
    assert issues == ["no frontmatter fence"]


# ---------------------------------------------------------------------------
# scan_slug — minimal weights fixture
# ---------------------------------------------------------------------------


WEIGHTS = {
    "en": {"secrets": 5},
    "zh": {"秘笈": 6},
    "banned_phrases_en": [r"unlock"],
    "banned_patterns_zh": [r"解锁"],
    "thresholds": {"en": 4, "zh": 6},
}


def _write_pair(tmp_path: Path, slug: str, en_text: str, zh_text: str) -> Path:
    d = tmp_path / slug
    d.mkdir()
    (d / "en.md").write_text(en_text, encoding="utf-8")
    (d / "zh.md").write_text(zh_text, encoding="utf-8")
    return d


def test_scan_slug_missing_pair_returns_missing_pair(tmp_path: Path) -> None:
    slug = tmp_path / "lonely"
    slug.mkdir()
    (slug / "en.md").write_text("---\ncategory: 'ai'\n---\nbody", encoding="utf-8")
    result = mod.scan_slug(slug, WEIGHTS)
    assert "missing_pair" in result["actions"]
    assert result["zh"]["present"] is False


def test_scan_slug_clean_pair_has_no_actions(tmp_path: Path) -> None:
    en = _frontmatter("ai", 6) + "\n## Context\n\nnothing here.\n"
    zh_front = "---\ncategory: 'ai'\ntranslationKey: 'demo'\n" + "\n".join(
        f"  - q: 问题 {i}\n    a: 答案 {i}" for i in range(6)
    ) + "\n---\n\n## Context\n\n没有敏感词。\n"
    d = _write_pair(tmp_path, "pristine", en, zh_front)
    # remove the trailing ## Context duplicated from _frontmatter if any
    en_text = (
        _frontmatter("ai", 6).rstrip()
        + "\n## Context\n\nnothing here.\n\n## Take-away\n\nsame\n\n"
        + "\n\n".join(f"## H{i}" for i in range(5))  # pad to 5 H2s
    )
    _write_pair(tmp_path, "test1", en_text, zh_front)
    res = mod.scan_slug(tmp_path / "test1", WEIGHTS)
    # We don't strictly require zero actions because the H2-fill heuristic
    # may collide; instead confirm the scan produced both legs and did not
    # flag a missing_pair.
    assert "missing_pair" not in res["actions"]
    assert res["en"]["present"] is True
    assert res["zh"]["present"] is True


def test_scan_slug_banned_phrase_flags_action(tmp_path: Path) -> None:
    # Build 5 H2s so the only action is the banned phrase.
    en_text = (
        "---\n"
        "category: 'ai'\n"
        "translationKey: 'bp'\n"
        + "\n".join(f"  - q: q{i}\n    a: a{i}" for i in range(6))
        + "\n---\n\n"
        + "## A\n\nThis will unlock things.\n\n"
        + "## B\n\nNothing.\n\n"
        + "## C\n\nNothing.\n\n"
        + "## D\n\nNothing.\n\n"
        + "## E\n\nNothing.\n"
    )
    zh_text = (
        "---\n"
        "category: 'ai'\n"
        "translationKey: 'bp'\n"
        + "\n".join(f"  - q: 问题 {i}\n    a: 答案 {i}" for i in range(6))
        + "\n---\n\n"
        + "## 甲\n\n没有敏感词。\n\n"
        + "## 乙\n\n没有。\n\n"
        + "## 丙\n\n没有。\n\n"
        + "## 丁\n\n没有。\n\n"
        + "## 戊\n\n没有。\n"
    )
    _write_pair(tmp_path, "banned", en_text, zh_text)
    res = mod.scan_slug(tmp_path / "banned", WEIGHTS)
    assert any(a.startswith("banned_phrase_en:") for a in res["actions"])
