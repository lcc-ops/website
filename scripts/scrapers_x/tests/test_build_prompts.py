"""Unit tests for scripts/auto/_build_prompts.py pure helpers.

Loads the module via importlib.util.spec_from_file_location so module-level
sqlite3 connection constants (ZSXQ_DB, X_DB, ...) do not actually open the
DBs at import time. We only exercise pure functions.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
AUTO_DIR = REPO_ROOT / "scripts" / "auto"
SRC = AUTO_DIR / "_build_prompts.py"


def _load():
    spec = importlib.util.spec_from_file_location("_build_prompts", SRC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("_build_prompts", mod)
    spec.loader.exec_module(mod)
    return mod


mod = _load()


# ---------------------------------------------------------------------------
# decode_mojibake
# ---------------------------------------------------------------------------


def test_decode_mojibake_round_trip_and_empty() -> None:
    # Bytes that were stored as if latin1 but are UTF-8: 'é”在' → utf8 bytes
    raw = "é”在".encode("utf-8").decode("latin1")
    assert mod.decode_mojibake(raw) == "é”在"
    assert mod.decode_mojibake(None) == ""
    assert mod.decode_mojibake("") == ""


# ---------------------------------------------------------------------------
# detect_niche
# ---------------------------------------------------------------------------


def test_detect_niche_first_match_returns_kw_key() -> None:
    assert mod.detect_niche("This person sells ebooks on kindle.") == "kdp"


def test_detect_niche_fallback_to_vertical_ai() -> None:
    assert mod.detect_niche("Just chatting about random stuff.") == "vertical-ai"


def test_detect_niche_case_insensitive() -> None:
    assert mod.detect_niche("Open Source GitHub stars monetization guide") == "open-source-monetize"


# ---------------------------------------------------------------------------
# slug_from_body
# ---------------------------------------------------------------------------


def test_slug_from_body_starts_with_niche() -> None:
    out = mod.slug_from_body("Build a $2k/month Shopify side hustle with AI tools.", "side-hustle")
    assert out.startswith("side-hustle-")
    assert len(out) <= 80


def test_slug_from_body_handles_cjk_only_input() -> None:
    out = mod.slug_from_body("用 AI 副业每月多赚三千块", "vertical-ai")
    assert out.startswith("vertical-ai-")
    assert "--" not in out  # collapsed dashes


def test_slug_from_body_never_returns_empty() -> None:
    # Even nonsense input falls back to '{niche}-case' rather than ''.
    out = mod.slug_from_body("", "vertical-ai")
    assert out
    assert out.startswith("vertical-ai-")


# ---------------------------------------------------------------------------
# dedup_slug
# ---------------------------------------------------------------------------


def test_dedup_slug_no_collision_returns_base(tmp_path: Path, monkeypatch) -> None:
    # Point the module at a tmp dir without mutating the module-level
    # constant in place across other tests.
    fake_root = tmp_path / "blog"
    fake_root.mkdir()
    monkeypatch.setattr(mod, "BLOG_ROOT", fake_root)
    slug = mod.dedup_slug("ai-tools-cool", "2026-07-15", set())
    assert slug == "ai-tools-cool"


def test_dedup_slug_appends_suffix_on_collision(tmp_path: Path, monkeypatch) -> None:
    fake_root = tmp_path / "blog"
    fake_root.mkdir()
    (fake_root / "ai-tools-cool").mkdir()
    monkeypatch.setattr(mod, "BLOG_ROOT", fake_root)
    slug = mod.dedup_slug("ai-tools-cool", "2026-07-15", set())
    assert slug == "ai-tools-cool-2026-07-15-01"
    slug2 = mod.dedup_slug("ai-tools-cool", "2026-07-15", {slug})
    assert slug2 == "ai-tools-cool-2026-07-15-02"


# ---------------------------------------------------------------------------
# hits_in_body
# ---------------------------------------------------------------------------


def test_hits_in_body_returns_every_keyword_match() -> None:
    out = mod.hits_in_body("Using Claude and Cursor side-by-side. My GPT-4o workflow.")
    # Order matches AI_KEYWORDS list.
    assert "Claude" in out
    assert "Cursor" in out
    assert "GPT-4o" in out


def test_hits_in_body_dedup_and_lowercased_body() -> None:
    out1 = mod.hits_in_body("prompt prompt Prompt")
    out2 = mod.hits_in_body("PROMPT")
    # "prompt" appears once in AI_KEYWORDS — duplicate input doesn't fan out.
    assert out1 == out2


# ---------------------------------------------------------------------------
# render_prompt
# ---------------------------------------------------------------------------


def test_render_prompt_substitutes_all_placeholders() -> None:
    template = (
        "src={SOURCE_TABLE} db={DB_PATH} id={ROW_ID} score={SCORE} "
        "niche={NICHE} hits={AI_KEYWORDS_HIT} pub={PUBDATE}"
    )
    c = mod.Candidate(
        source_table="x",
        row_id="42",
        score=10,
        body="x",
        niche="kdp",
        posted_at="2026-07-15",
        ai_keywords_hit=["Claude", "GPT"],
    )
    out = mod.render_prompt(template, c, "2026-07-15")
    assert "{SOURCE_TABLE}" not in out
    assert "{DB_PATH}" not in out
    assert out.startswith("src=x db=")
    assert "niche=kdp hits=Claude, GPT pub=2026-07-15" in out


def test_render_prompt_falls_back_to_paren_none_when_no_hits() -> None:
    template = "{AI_KEYWORDS_HIT}"
    c = mod.Candidate(
        source_table="zsxq",
        row_id="1",
        score=0,
        body="",
        niche="vertical-ai",
        posted_at="",
        ai_keywords_hit=[],
    )
    assert mod.render_prompt(template, c, "2026-07-15") == "(none)"
