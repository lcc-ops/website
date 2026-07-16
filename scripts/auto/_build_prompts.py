"""Build per-candidate prompt JSON files for the headless-Claude batch.

Reads both SQLite databases (zsxq, x), picks top candidates within the last
24 hours above an engagement threshold, then writes one JSON file per
candidate into _queue/ ready for _draft_one.ps1 to consume.

Two parallel tracks:
  - ai:      AI-monetization posts (legacy behavior). Uses the AI-keyword
             whitelist and `_prompts/draft_one_topic.md` (category='ai').
  - general: Non-AI operator-notes posts. Uses the AI-keyword blocklist plus
             a general-niche whitelist and `_prompts/draft_one_topic_general.md`
             (category set per niche via NICHE_TO_CATEGORY).
  - both:    Merge both streams, capped at --top per source per track.

Each candidate's queue JSON carries the rendered `prompt` (template +
substitutions), so `_draft_one.ps1` does not need to know which track it is
on — it just reads `payload.prompt` and ships it to `claude.cmd -p`.

Dedup vs state.json.last_slugs so we don't redraft. Slug collision with an
existing folder under src/content/blog/ gets a -YYYYMMDD-NN suffix.

Exits 0 with an empty queue if no candidates pass.

Run: python scripts/auto/_build_prompts.py [--since-hours 24] [--top 5]
                                 [--track ai|general|both]
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, timedelta, timezone


REPO = Path(__file__).resolve().parents[2]
ZSXQ_DB = REPO / "scripts" / "scrapers" / "data" / "zsxq.sqlite3"
X_DB = REPO / "scripts" / "scrapers_x" / "data" / "x.sqlite3"
PROMPT_TEMPLATES: dict[str, Path] = {
    "ai": REPO / "scripts" / "auto" / "_prompts" / "draft_one_topic.md",
    "general": REPO / "scripts" / "auto" / "_prompts" / "draft_one_topic_general.md",
}
QUEUE = REPO / "scripts" / "auto" / "_queue"
STATE = REPO / "scripts" / "auto" / "state.json"
BLOG_ROOT = REPO / "src" / "content" / "blog"

# Map general-track niche -> category written into frontmatter. Kept in sync
# with the actual categories already present under src/content/blog/ (see
# README "Category coverage" for the live distribution).
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

# Mirror of scripts/scrapers_x/_lib/selectors.NICHE_TO_QUERY for the
# general-track niches. Used by tests to assert the two sides agree; the
# runtime crawler re-imports the canonical version from selectors at run
# time, so this dict must be kept structurally aligned (same keys, but the
# query strings may legitimately differ — the test only checks key set).
#
# NOTE: the 'ai' niche lives in the x crawler (legacy AI-monetization
# query) but not in this file because the AI track is the legacy surface
# that does not need a niche->category lookup here.
NICHE_SEARCH_KEYWORDS: dict[str, str] = {
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

# AI-keyword list: union of what's in references/keyword_list.md (skill) and
# scripts/check/step3d__list_x_wider.py. The set drives two jobs:
#   1) ai-track: drop candidates whose body has none of these
#   2) general-track: drop candidates whose body has any of these (the post
#      is too AI-centric for a non-AI category)
#   3) we hand the hits list back to the ai-track prompt so Claude sees
#      which key fired
AI_KEYWORDS: list[str] = [
    "AI", "GPT", "Claude", "LLM", "agent", "智能体",
    "Seedance", "Sora", "Veo", "Kling", "Suno", "Udio",
    "Midjourney", "ComfyUI", "Stable Diffusion", "GPTs", "ChatGPT",
    "Gemini", "DeepSeek", "Cursor", "Copilot", "Coze",
    "n8n", "Make", "Zapier", "GPT-4o", "GPT-5", "o1", "o3",
    "数字人", "AI 变现", "AI 副业", "AI 工具", "RAG", "Workflow",
    "Sonnet", "Opus", "Haiku", "prompt", "提示词", "知识库",
    "模型", "大模型", "Embedding", "向量", "lora", "fine", "tune",
]

# Niches the AI-track prompt maps AI-keyword hits to. Keep kebab-ish.
AI_NICHE_KEYWORDS: dict[str, list[str]] = {
    "kdp": ["kdp", "kindle", "ebook", "电子出书", "亚马逊出版"],
    "seedance": ["seedance", "sora", "veo", "kling", "AI 视频", "AI视频"],
    "fanvue": ["fanvue", "onlyfans", "patreon", "成人内容", "AI美女"],
    "etsy": ["etsy", "etsy SEO", "etsy选品"],
    "tiktok-shop": ["tiktok shop", "tiktok小店", "tk小店"],
    "etsy-pod": ["print on demand", "pod", "POD"],
    "side-hustle": ["副业", "side hustle", "薅羊毛"],
    "open-source-monetize": ["github stars", "open source", "开源变现", "sponsor"],
    "medium-seo": ["medium", "substack", "SEO content"],
    "youtube-faceless": ["faceless youtube", "无人出镜", "youtube automation"],
    "podcast": ["podcast", "播客"],
    "ai-agents": ["ai agent", "智能体", "agent"],
    "rag": ["rag", "知识库", "vector store"],
    "llm-finetune": ["fine", "tune", "lora", "微调"],
}

# Niches the general-track prompt maps non-AI body to. Each maps via
# NICHE_TO_CATEGORY to one of the existing non-AI frontmatter categories
# (payment / pricing / shipping / ops / ads).
GENERAL_NICHE_KEYWORDS: dict[str, list[str]] = {
    "logistics": ["物流", "物流成本", "小包", "epacket", "ePacket", "跨境物流"],
    "cbm": ["cbm", "抛货", "重货", "dimensional weight", "体积重"],
    "payment-fees": ["支付手续费", "支付通道", "费率", "通道费"],
    "chargeback": ["chargeback", "拒付", "拒赔", "dispute", "撤单"],
    "global-payments": ["跨境支付", "local payment", "本地支付", "global payment"],
    "paypal-stripe": ["paypal", "stripe", "贝宝", "条纹"],
    "ecommerce-fees": ["平台费", "佣金", "佣金率", "marketplace fee"],
    "etsy-pricing": ["etsy fee", "etsy 费用", "etsy 佣金"],
    "shopify-pricing": ["shopify pricing", "shopify 订阅", "shopify plan"],
    "amazon-pricing": ["amazon fba", "fba fee", "fba 费用", "fba 仓储"],
    "dropshipping-costs": ["dropshipping", "dropship", "无货源", "一件代发"],
    "google-ads": ["google ads", "roas", "roi", "广告投放", "投产比"],
    "freelance-pricing": ["freelancer", "自由职业", "外包定价", "按月收费"],
    "ops-tools": ["crm", "工单系统", "客户管理", "客户运营"],
    "lead-gen": ["销售线索", "leads broker", "线索中介", "leads broker"],
    "podcast-monetize": ["播客变现", "播客广告", "听众打赏", "podcast sponsor"],
    "youtube-creator": ["youtube 收益", "cpm", "youtube partner"],
}


@dataclass(frozen=True)
class Candidate:
    source_table: str
    row_id: str
    score: int
    body: str
    niche: str
    posted_at: str
    ai_keywords_hit: list[str] = field(default_factory=list)


def decode_mojibake(s: str | None) -> str:
    """Body text is GBK-as-latin1; round-trip back to UTF-8."""
    if not s:
        return ""
    try:
        return s.encode("latin1").decode("utf-8")
    except Exception:
        return s or ""


def load_state() -> dict:
    if not STATE.exists():
        return {"last_run_date": None, "last_slugs": [], "draft_status": {}}
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"last_run_date": None, "last_slugs": [], "draft_status": {}}


def _keyword_matches(keyword: str, body_lower: str) -> bool:
    """True if `keyword` appears in `body_lower`.

    For Latin/CJK keywords, we use a regex with word boundaries. CJK has no
    word boundary concept, so we only apply \\b when the keyword is purely
    ASCII Latin. This prevents "AI" from matching "trail/paid/detail" while
    still matching "AI" / "AI agent" / "AI变现".
    """
    if not keyword:
        return False
    kw = keyword.lower()
    is_ascii_latin = all(c.isascii() and c.isalpha() or c in "-_" for c in kw)
    if is_ascii_latin:
        return re.search(rf"(?<![A-Za-z0-9]){re.escape(kw)}(?![A-Za-z0-9])", body_lower) is not None
    return kw in body_lower


def detect_niche(body: str, table: dict[str, list[str]], fallback: str = "") -> str:
    """Pick the first niche whose any keyword appears in `body`.

    Latin keywords are matched as whole words (\\b boundaries) to avoid
    "AI" matching "trail/paid/detail". CJK keywords (no word boundary
    concept) still match as substrings.

    `fallback` is returned when nothing matches. Pass "vertical-ai" for the
    AI track so an AI-themed post that doesn't trip any AI_NICHE_KEYWORDS
    still gets a niche; pass "" for the general track so a body that
    matches no general niche is rejected by the caller."""
    lower = body.lower()
    for niche, kws in table.items():
        for kw in kws:
            if _keyword_matches(kw, lower):
                return niche
    return fallback


def slug_from_body(body: str, niche: str) -> str:
    """Make a 3-6 word kebab slug from the first non-empty line + niche.

    Latin tokens are dashes; Chinese runs are joined into single segments
    (each segment a short noun phrase). Total head part is capped at ~30
    chars so the final slug stays readable.
    """
    first = next(
        (line.strip() for line in body.splitlines() if line.strip() and not line.strip().startswith("#")),
        body[:200],
    )
    first = re.sub(r"http\S+", "", first)

    # Split into alternating runs of CJK / non-CJK so we can group CJK
    # into 2-4 character phrases (more readable than single-char slugs).
    parts = re.findall(r"[一-鿿]+|[^一-鿿]+", first)
    segments: list[str] = []
    cjk_buf: list[str] = []
    total_units = 0
    for p in parts:
        if re.match(r"^[一-鿿]+$", p):
            for ch in p:
                cjk_buf.append(ch)
                if len(cjk_buf) == 3:
                    seg = "".join(cjk_buf)
                    if seg not in segments:
                        segments.append(seg)
                    cjk_buf = []
                    total_units += 3
                    if total_units >= 18 or len(segments) >= 3:
                        break
        else:
            if cjk_buf:
                seg = "".join(cjk_buf)
                if seg not in segments:
                    segments.append(seg)
                cjk_buf = []
                total_units += len(seg)
            # Pull candidate latin tokens (>=3 chars).
            for m in re.finditer(r"[A-Za-z][A-Za-z0-9-]{2,}", p):
                tok = m.group(0).lower()
                if tok in {"this", "that", "with", "from", "have", "were", "they",
                           "their", "what", "when", "where", "which", "would",
                           "could", "should", "about", "your", "will", "into", "than"}:
                    continue
                if tok == niche or tok in segments:
                    continue
                segments.append(tok)
                total_units += len(tok)
                if total_units >= 24 or len(segments) >= 4:
                    break
        if total_units >= 24 or len(segments) >= 4:
            break
    if cjk_buf and len(segments) < 4:
        segments.append("".join(cjk_buf))

    if not segments:
        segments = ["case"]
    head = "-".join(segments[:4])
    head = re.sub(r"-+", "-", head).strip("-")
    head = head[:36]
    slug = f"{niche}-{head}"[:80].strip("-")
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or niche


def dedup_slug(slug: str, today: str, taken: set[str]) -> str:
    """If the candidate slug already exists as a folder or is reserved by an
    earlier queue entry this run, append -YYYYMMDD-NN until unique."""
    candidate = slug
    suffix = 1
    while (BLOG_ROOT / candidate).exists() or candidate in taken:
        candidate = f"{slug}-{today}-{suffix:02d}"
        suffix += 1
    return candidate


def hits_in_body(body: str) -> list[str]:
    """Return the AI_KEYWORDS entries that appear in `body`.

    Same word-boundary treatment as detect_niche: Latin keywords are matched
    with \\b; CJK keywords match as substrings."""
    lower = body.lower()
    return [k for k in AI_KEYWORDS if _keyword_matches(k, lower)]


def zsxq_candidates(since_hours: int, threshold: int, track: str) -> list[Candidate]:
    """track='ai' keeps body that contains AI_KEYWORDS.
    track='general' keeps body that contains NO AI_KEYWORDS but matches a
    GENERAL_NICHE_KEYWORDS entry. track='both' applies both filters to two
    independent streams merged in main()."""
    if not ZSXQ_DB.exists():
        return []
    con = sqlite3.connect(f"file:{ZSXQ_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
    rows = con.execute(
        """
        SELECT topic_id, posted_at, like_count, comment_count, body_text
        FROM topics
        WHERE last_seen_at >= ?
          AND body_text IS NOT NULL
          AND body_text != ''
        """,
        (cutoff,),
    ).fetchall()
    enriched: list[Candidate] = []
    for r in rows:
        body = decode_mojibake(r["body_text"])
        score = (r["like_count"] or 0) * 2 + (r["comment_count"] or 0) * 3
        if score < threshold:
            continue
        hit = hits_in_body(body)
        if track in ("ai", "both") and not hit:
            continue
        if track in ("general", "both") and hit:
            continue
        if track in ("general", "both"):
            niche = detect_niche(body, GENERAL_NICHE_KEYWORDS, fallback="")
            if not niche:
                continue
        else:
            niche = detect_niche(body, AI_NICHE_KEYWORDS, fallback="vertical-ai")
        enriched.append(
            Candidate(
                source_table="zsxq",
                row_id=r["topic_id"],
                score=score,
                body=body,
                niche=niche,
                posted_at=r["posted_at"],
                ai_keywords_hit=hit,
            )
        )
    con.close()
    enriched.sort(key=lambda c: (-c.score, c.posted_at))
    return enriched


def x_candidates(since_hours: int, threshold: int, track: str) -> list[Candidate]:
    if not X_DB.exists():
        return []
    # Reverse map: x.com query string -> niche. Built lazily so an import
    # failure / missing selectors is not fatal here — without it the
    # function falls back to body-only niche detection (the pre-change
    # behavior).
    query_to_niche: dict[str, str] = {}
    try:
        import importlib.util as _ilu
        _x_selectors = REPO / "scripts" / "scrapers_x" / "_lib" / "selectors.py"
        if _x_selectors.exists():
            _spec = _ilu.spec_from_file_location("x_selectors_under_build", _x_selectors)
            if _spec and _spec.loader:
                _mod = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_mod)
                query_to_niche = {q: n for n, q in _mod.NICHE_TO_QUERY.items()}
    except Exception:
        query_to_niche = {}

    con = sqlite3.connect(f"file:{X_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
    rows = con.execute(
        """
        SELECT tweet_id, like_count, reply_count, quote_count, repost_count,
               body_text, posted_at, search_keyword
        FROM topics
        WHERE last_seen_at >= ?
          AND body_text IS NOT NULL
          AND body_text != ''
        """,
        (cutoff,),
    ).fetchall()
    enriched: list[Candidate] = []
    for r in rows:
        body = decode_mojibake(r["body_text"])
        likes = r["like_count"] or 0
        replies = r["reply_count"] or 0
        quotes = r["quote_count"] or 0
        reposts = r["repost_count"] or 0
        score = likes * 2 + replies * 3 + quotes * 2 + reposts
        if score < threshold:
            continue
        hit = hits_in_body(body)
        if track in ("ai", "both") and not hit:
            continue
        if track in ("general", "both") and hit:
            continue
        if track in ("general", "both"):
            niche = detect_niche(body, GENERAL_NICHE_KEYWORDS, fallback="")
            # Fallback: if the body doesn't trip any GENERAL_NICHE_KEYWORDS
            # but the post was crawled under a known non-AI x.com query,
            # trust the source niche so the per-niche crawl isn't wasted.
            if not niche:
                src_niche = query_to_niche.get(r["search_keyword"] or "", "")
                if src_niche and src_niche != "ai":
                    niche = src_niche
            if not niche:
                continue
        else:
            niche = detect_niche(body, AI_NICHE_KEYWORDS, fallback="vertical-ai")
        enriched.append(
            Candidate(
                source_table="x",
                row_id=r["tweet_id"],
                score=score,
                body=body,
                niche=niche,
                posted_at=r["posted_at"],
                ai_keywords_hit=hit,
            )
        )
    con.close()
    enriched.sort(key=lambda c: (-c.score, c.posted_at))
    return enriched


def render_prompt(template: str, c: Candidate, pub_date: str, track: str) -> str:
    db_path = str(ZSXQ_DB if c.source_table == "zsxq" else X_DB)
    category = "ai" if track == "ai" else NICHE_TO_CATEGORY.get(c.niche, "pricing")
    return (
        template
        .replace("{SOURCE_TABLE}", c.source_table)
        .replace("{DB_PATH}", db_path)
        .replace("{ROW_ID}", c.row_id)
        .replace("{SCORE}", str(c.score))
        .replace("{NICHE}", c.niche)
        .replace("{CATEGORY}", category)
        .replace("{AI_KEYWORDS_HIT}", ", ".join(c.ai_keywords_hit) or "(none)")
        .replace("{PUBDATE}", pub_date)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since-hours", type=int, default=24)
    parser.add_argument("--top", type=int, default=5, help="Per source table")
    parser.add_argument("--threshold", type=int, default=6)
    parser.add_argument(
        "--track",
        choices=("ai", "general", "both"),
        default="both",
        help="ai = AI-only (legacy). general = non-AI topics only. both = "
             "merge both streams, capped at --top per source. Default "
             "'both' keeps schtasks-driven behavior unchanged in count.",
    )
    args = parser.parse_args()

    state = load_state()
    already_drafted = set(state.get("last_slugs", []))

    if not PROMPT_TEMPLATES["ai"].exists():
        print(f"ai prompt template missing: {PROMPT_TEMPLATES['ai']}", file=sys.stderr)
        return 1
    if args.track in ("general", "both") and not PROMPT_TEMPLATES["general"].exists():
        print(f"general prompt template missing: {PROMPT_TEMPLATES['general']}", file=sys.stderr)
        return 1

    templates = {k: v.read_text(encoding="utf-8") for k, v in PROMPT_TEMPLATES.items()}

    if args.track == "ai":
        zsxq = [c for c in zsxq_candidates(args.since_hours, args.threshold, "ai")
                if c.row_id not in already_drafted][: args.top]
        xcand = [c for c in x_candidates(args.since_hours, args.threshold, "ai")
                 if c.row_id not in already_drafted][: args.top]
    elif args.track == "general":
        zsxq = [c for c in zsxq_candidates(args.since_hours, args.threshold, "general")
                if c.row_id not in already_drafted][: args.top]
        xcand = [c for c in x_candidates(args.since_hours, args.threshold, "general")
                 if c.row_id not in already_drafted][: args.top]
    else:
        zsxq = [c for c in zsxq_candidates(args.since_hours, args.threshold, "ai")
                if c.row_id not in already_drafted][: args.top]
        xcand = [c for c in x_candidates(args.since_hours, args.threshold, "ai")
                 if c.row_id not in already_drafted][: args.top]
        zsxq_g = [c for c in zsxq_candidates(args.since_hours, args.threshold, "general")
                  if c.row_id not in already_drafted][: args.top]
        xcand_g = [c for c in x_candidates(args.since_hours, args.threshold, "general")
                   if c.row_id not in already_drafted][: args.top]
        zsxq = zsxq + zsxq_g
        xcand = xcand + xcand_g

    candidates = zsxq + xcand
    if not candidates:
        print("no candidates with score>=threshold; nothing to draft.")
        return 0

    QUEUE.mkdir(parents=True, exist_ok=True)
    # Clear stale queue files from prior runs.
    for old in QUEUE.glob("*.json"):
        try:
            old.unlink()
        except OSError:
            pass

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    taken: set[str] = set()

    queued: list[dict] = []
    for c in candidates:
        track = (
            "ai"
            if c.niche in AI_NICHE_KEYWORDS or c.niche == "vertical-ai"
            else "general"
        )
        slug = dedup_slug(slug_from_body(c.body, c.niche), today, taken)
        taken.add(slug)
        prompt = render_prompt(templates[track], c, pub_date, track)
        payload = {
            "slug": slug,
            "source_table": c.source_table,
            "row_id": c.row_id,
            "score": c.score,
            "niche": c.niche,
            "track": track,
            "category": "ai" if track == "ai" else NICHE_TO_CATEGORY.get(c.niche, "pricing"),
            "ai_keywords_hit": c.ai_keywords_hit,
            "posted_at": c.posted_at,
            "pubDate": pub_date,
            "prompt": prompt,
        }
        out = QUEUE / f"{c.source_table}__{c.row_id}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        queued.append({"slug": slug, "source": c.source_table, "row_id": c.row_id,
                       "score": c.score, "track": track,
                       "category": payload["category"]})

    summary_path = QUEUE / "_summary.json"
    summary_path.write_text(json.dumps(queued, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"queued": queued, "count": len(queued)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
