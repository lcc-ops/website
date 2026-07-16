"""Anti-AI-vocab check on freshly drafted <slug>/{en,zh}.md.

Reads the 5 H2 section structure, scans each <slug>/{en,zh}.md against
weights.json + banned-phrase regex, and flags contaminated slugs.

Contaminated slugs are reported in the JSON output ONLY. They are NOT
moved to _archive/ — a single full-fail sweep can wipe every article from
src/content/blog/ in one go, and that is not a reversible action from
the operator's perspective. A human (or a later review step) decides
what to do with contaminated slugs.

Category check: each slug's expected category is derived from the niche tag
(= tags[0] in frontmatter) via the NICHE_TO_CATEGORY table mirrored from
_build_prompts. The ai-track still hard-codes 'ai' as the expected category;
the general-track uses the dynamic lookup. Either 'ai' or any value present
in the lookup passes the frontmatter gate; anything else is contaminated.

Returns exit 0 with a JSON report on stdout; the parent _build_and_summarize.ps1
reads the report to decide whether the run is salvageable.

Run: python scripts/auto/_anti_ai_check.py [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
BLOG_ROOT = REPO / "src" / "content" / "blog"
ARCHIVE = REPO / "scripts" / "auto" / "_archive"
WEIGHTS = REPO / "scripts" / "auto" / "weights.json"

REQUIRED_SECTIONS = ("Context", "What this case does not cover", "Take-away")

# AI-track posts use the English H2 names exactly. General-track posts are
# expected to have the *translated* H2 names (zh 背景 / 这个案例没覆盖的部分 /
# 结论 for the three required anchors), so we check those instead when the
# slug's frontmatter category is one of the general categories.
GENERAL_REQUIRED_SECTIONS_ZH: dict[str, dict[str, str]] = {
    "payment":  {"context": "背景", "gaps": "这个案例没覆盖的部分", "takeaway": "结论"},
    "pricing":  {"context": "背景", "gaps": "这个案例没覆盖的部分", "takeaway": "结论"},
    "shipping": {"context": "背景", "gaps": "这个案例没覆盖的部分", "takeaway": "结论"},
    "ops":      {"context": "背景", "gaps": "这个案例没覆盖的部分", "takeaway": "结论"},
    "ads":      {"context": "背景", "gaps": "这个案例没覆盖的部分", "takeaway": "结论"},
}

# Mirrors _build_prompts.NICHE_TO_CATEGORY. Kept as a literal here so this
# script is self-contained (no relative import); the test in
# tests/test_general_track_category.py asserts the two stay in sync.
NICHE_TO_CATEGORY: dict[str, str] = {
    "logistics": "shipping",
    "cbm": "shipping",
    "payment-fees": "payment",
    "chargeback": "payment",
    "global-payments": "payment",
    "paypal-stripe": "payment",
    "ecommerce-fees": "pricing",
    "etsy-pricing": "pricing",
    "shopify-pricing": "pricing",
    "amazon-pricing": "pricing",
    "dropshipping-costs": "pricing",
    "google-ads": "ads",
    "freelance-pricing": "pricing",
    "ops-tools": "ops",
    "lead-gen": "ops",
    "podcast-monetize": "pricing",
    "youtube-creator": "pricing",
}


def count_words(text: str, terms: list[str]) -> dict[str, int]:
    """Count occurrences of each term in `text`, case-insensitive (en side)."""
    counts: dict[str, int] = {}
    lower = text.lower()
    for t in terms:
        if not t:
            continue
        c = lower.count(t.lower())
        if c:
            counts[t] = c
    return counts


def section_word_count(body: str) -> dict[str, int]:
    """Return word count for each ## heading → next H2."""
    sections: dict[str, int] = {}
    cur_h: str | None = None
    cur_text: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur_h is not None:
                sections[cur_h] = len(" ".join(cur_text).split())
            cur_h = m.group(1).strip()
            cur_text = []
        else:
            cur_text.append(line)
    if cur_h is not None:
        sections[cur_h] = len(" ".join(cur_text).split())
    return sections


def has_banned_phrase(text: str, phrases: list[str]) -> list[str]:
    hits: list[str] = []
    for p in phrases:
        if p and re.search(p, text, flags=re.IGNORECASE):
            hits.append(p)
    return hits


def expected_category_from_niche(text: str) -> str | None:
    """Return the category a slug *should* have, based on its tags[0] niche.

    Returns 'ai' for the AI track (no niche match in NICHE_TO_CATEGORY).
    Returns the mapped value for any general-track niche.
    Returns None if tags[0] is missing or unparseable (caller should treat as
    contaminated).
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    tags_m = re.search(r"^tags:\s*\[(.*?)\]\s*$", fm, flags=re.MULTILINE | re.DOTALL)
    if not tags_m:
        return None
    first = tags_m.group(1).split(",")[0].strip().strip("'\"")
    if not first:
        return None
    if first in NICHE_TO_CATEGORY:
        return NICHE_TO_CATEGORY[first]
    return "ai"


def frontmatter_ok(text: str) -> tuple[bool, list[str]]:
    """Return (ok, list-of-issues). Verifies 6 FAQ entries and the
    category matches what the niche tag implies."""
    issues: list[str] = []
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not m:
        return False, ["no frontmatter fence"]
    fm = m.group(1)
    expected = expected_category_from_niche(text)
    cat_m = re.search(r"^category:\s*['\"]([^'\"]+)['\"]\s*$", fm, flags=re.MULTILINE)
    if not cat_m:
        issues.append("category missing")
    else:
        actual = cat_m.group(1)
        if expected is None:
            issues.append(f"cannot derive expected category from tags[0]")
        elif actual != expected:
            issues.append(f"category is '{actual}', expected '{expected}'")
    faq_matches = re.findall(r"^\s*-\s*q:\s*.+$", fm, flags=re.MULTILINE)
    if len(faq_matches) != 6:
        issues.append(f"FAQ entries = {len(faq_matches)}, expected 6")
    if "translationKey:" not in fm:
        issues.append("missing translationKey")
    return not issues, issues


def scan_slug(slug: Path, weights: dict) -> dict:
    en = slug / "en.md"
    zh = slug / "zh.md"
    result: dict = {"slug": slug.name, "en": None, "zh": None, "actions": []}

    en_text = en.read_text(encoding="utf-8") if en.exists() else ""
    zh_text = zh.read_text(encoding="utf-8") if zh.exists() else ""

    if not en_text or not zh_text:
        result["actions"].append("missing_pair")
        if not en_text:
            result["en"] = {"present": False}
        if not zh_text:
            result["zh"] = {"present": False}
        return result

    result["en"] = {"present": True}
    result["zh"] = {"present": True}

    en_fm_ok, en_fm_issues = frontmatter_ok(en_text)
    zh_fm_ok, zh_fm_issues = frontmatter_ok(zh_text)
    if not en_fm_ok:
        result["actions"].append(f"frontmatter_en:{','.join(en_fm_issues)}")
    if not zh_fm_ok:
        result["actions"].append(f"frontmatter_zh:{','.join(zh_fm_issues)}")

    en_body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", en_text, count=1, flags=re.DOTALL)
    zh_body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", zh_text, count=1, flags=re.DOTALL)

    en_terms = list(weights["en"].keys())
    zh_terms = list(weights["zh"].keys())
    en_hits = count_words(en_body, en_terms)
    zh_hits = count_words(zh_body, zh_terms)

    en_score = sum(weights["en"].get(w, 1) * c for w, c in en_hits.items())
    zh_score = sum(weights["zh"].get(w, 1) * c for w, c in zh_hits.items())

    result["en"]["score"] = en_score
    result["en"]["hits"] = en_hits
    result["zh"]["score"] = zh_score
    result["zh"]["hits"] = zh_hits

    th = weights["thresholds"]
    if en_score >= th["en"]:
        result["actions"].append(f"en_weighted_ge_{th['en']}")
    if zh_score >= th["zh"]:
        result["actions"].append(f"zh_weighted_ge_{th['zh']}")

    banned_en = has_banned_phrase(en_body, weights["banned_phrases_en"])
    banned_zh = has_banned_phrase(zh_body, weights["banned_patterns_zh"])
    if banned_en:
        result["actions"].append("banned_phrase_en:" + "|".join(banned_en))
    if banned_zh:
        result["actions"].append("banned_phrase_zh:" + "|".join(banned_zh))

    en_sections = section_word_count(en_body)
    zh_sections = section_word_count(zh_body)
    missing_en = [s for s in REQUIRED_SECTIONS if s not in en_sections]
    if missing_en:
        result["actions"].append(f"missing_sections_en:{','.join(missing_en)}")

    # zh side: anchor on category. ai -> require same 3 English anchors (LLM
    # failed to translate). general -> require the 3 translated anchors for
    # that category.
    cat_m = (
        re.search(r"^category:\s*['\"]([^'\"]+)['\"]", en_text, flags=re.MULTILINE) or
        re.search(r"^category:\s*['\"]([^'\"]+)['\"]", zh_text, flags=re.MULTILINE)
    )
    cat_value = cat_m.group(1) if cat_m else ""
    if cat_value == "ai":
        missing_zh = [s for s in REQUIRED_SECTIONS if s not in zh_sections]
    elif cat_value in GENERAL_REQUIRED_SECTIONS_ZH:
        anchors = GENERAL_REQUIRED_SECTIONS_ZH[cat_value]
        missing_zh = [
            name for name, anchor in anchors.items() if anchor not in zh_sections
        ]
    else:
        missing_zh = []
    if missing_zh:
        result["actions"].append(f"missing_sections_zh:{','.join(missing_zh)}")

    h2_en = sum(1 for line in en_text.splitlines() if line.startswith("## "))
    h2_zh = sum(1 for line in zh_text.splitlines() if line.startswith("## "))
    if h2_en != 5:
        result["actions"].append(f"en_h2_count_{h2_en}")
    if h2_zh != 5:
        result["actions"].append(f"zh_h2_count_{h2_zh}")

    result["en"]["sections"] = en_sections
    result["zh"]["sections"] = zh_sections
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", default="")
    args = parser.parse_args()

    if not WEIGHTS.exists():
        print(f"weights file missing: {WEIGHTS}", file=sys.stderr)
        return 1
    weights = json.loads(WEIGHTS.read_text(encoding="utf-8"))

    if not BLOG_ROOT.exists():
        print(f"blog root missing: {BLOG_ROOT}", file=sys.stderr)
        return 1

    today = args.today or __import__("datetime").datetime.now().strftime("%Y-%m-%d")
    slug_dirs = [p for p in BLOG_ROOT.iterdir() if p.is_dir()]
    if not slug_dirs:
        print("no slugs in src/content/blog/; nothing to check.")
        print(json.dumps({"contaminated": [], "clean": []}))
        return 0

    clean: list[dict] = []
    contaminated: list[dict] = []
    for slug_dir in slug_dirs:
        result = scan_slug(slug_dir, weights)
        if result["actions"]:
            contaminated.append(result)
        else:
            clean.append({"slug": result["slug"], "en_score": result["en"]["score"], "zh_score": result["zh"]["score"]})

    # Move-to-archive behavior is disabled. The check now only *reports* the
    # contaminated slugs in its JSON output; an operator (or a later review
    # step) decides what to do with them. Rationale: a single full-fail
    # sweep can wipe every article from src/content/blog/ in one go, and
    # that is not a reversible action from the operator's perspective.
    # Re-enable only with explicit approval.

    report = {
        "today": today,
        "scanned": len(slug_dirs),
        "clean": clean,
        "contaminated": contaminated,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
