# Tone guide for AI Lab blog posts

The AI Lab section is **cold-eyed case-study collection**. The project explicitly
avoids hype and sponsored rankings. Read at least 2 of the existing 5 posts
before drafting so you can match the voice.

Reference posts to match:
- `src/content/blog/seedance-2-product-video-case/en.md`
- `src/content/blog/kdp-ai-ebook-case/en.md`
- `src/content/blog/vertical-ai-tools-gap/en.md`
- `src/content/blog/etsy-ai-digital-products/en.md`
- `src/content/blog/english-ai-seo-content-site/en.md`

## Hard rule: no author / source / original-post attribution

The published AI Lab posts **must not contain any attribution to a specific
author, knowledge-planet group, original post, or source URL.** Specifically,
do NOT include:

- author name (e.g., "静水流深", "a Chinese operator")
- group / planet name (e.g., "AI出海·1001个赚钱案例")
- group_id, topic_id, or any numeric platform identifier
- "posted on YYYY-MM-DD by ..." lines
- "Source: linked from a public post in ..." footer paragraphs
- "原帖", "source post", "case is from the web" framing

The case reads as if the writer is documenting the model directly. The
actual provenance is internal data — the writer knows where the case came
from, but the reader doesn't need to.

**Exception**: the post URL (e.g., `https://x.com/<handle>/status/<id>`)
is a structural reference, not an attribution. Don't include it either,
unless the writer specifically asks for it.

**On committing and pushing**: when Step 6 generates output, the
provenance detail (tweet_id, author handle, post URL) is held **only**
in the operator's working memory (or in `scripts/scrapers_x/data/x.sqlite3`).
It does NOT appear in the published markdown.

## Voice rules

1. **No AI hype.** Never write "AI is amazing", "revolutionary", "the future".
2. **No first-person claims of running products.** The skill author runs the
   AI Lab and explicitly states "cases are sourced from the web, I do not run
   AI products."
3. **Numbers with units, every time.** "€18,000 over 6 months" not "made a lot."
4. **Honest gaps.** Every post must include a "what the source does not cover"
   or "what the post does not cover" section. List 3-5 real gaps (taxes,
   dispute rates, account risk, distribution cost, etc.).

## Banned phrases (AI-tell words)

These phrases read as LLM-written when overused. **Do not use more than once per post**, and prefer zero:

- `cold read` / `cold-eyed` / `cold read of`
- `structural claim` / `structural argument` / `structural lesson` / `structural framing` / `structural point`
- `the mechanism` / `the mechanism is` / `mechanism:`
- `math-driven` / `math-driven when possible`
- `honest gaps` / `honest gap`
- `take-away` → use `bottom line` (en) / `带走就一句` (zh) instead
- `the case is not X. The case is Y` → rewrite as a single sentence, or `It is not X. It is Y.`
- `below is` → drop entirely; just start the next paragraph
- `the case lands on` / `the case frames` / `the case quietly skips` → use the verb on the noun directly
- `gig` (used as "side business" or "side hustle") → use `business` / `生意` / `项目` instead
- `leverage` as a verb or noun in any form → use `edge` / `杠杆` only when a Chinese operator said it
- `optimize` / `optimization` / `prioritize` / `landscape` (singular noun) / `harness` (verb) / `robust` / `seamless` / `holistic` → delete on sight

## Banned patterns

- The `**Structural claim**: ... **Structural lesson**: ...` two-paragraph block. Use one paragraph.
- The "table-then-paragraph" opener that re-explains the table. The table stands alone.
- Three or four `**Bold lead-in**: explanation.` items in a row (more than 3 in any section).
- `the case is not X. The case is Y` as a section opener more than once per post.
- Starting a sentence with `It is` three times in one paragraph.

## Self-check before writing

Before declaring a post done, run this mental grep:

1. Count `the case is` — if more than 1, rewrite the others
2. Count `structural` — should be 0
3. Count `mechanism` — should be 0 (or 1, with a different framing)
4. Count `cold read` / `cold-eyed` — should be 0
5. Count `gig` — should be 0
6. Scan first 3 sentences of every section — none should start with "The case is", "It is", or "Below is"

## Language register

- **en.md**: Plain professional English. Avoid American business jargon
  ("disrupt", "leverage", "synergy"). Prefer concrete verbs and unit-bound
  numbers.
- **zh.md**: Match the existing Chinese voice. Plainspoken, math-driven,
  no buzzwords. Use 半角 punctuation following the existing posts.

## What NOT to add

- No AI illustrations, no "image of the dashboard", no charts or graphs.
- No CTAs to "subscribe to our newsletter", no affiliate links.
- No call-to-action buttons in the body.
- No footer marketing block.

## What MUST be present

- Frontmatter with category: 'ai' (so the chip filter on /content works).
- `translationKey` identical to slug.
- tldr field with 1-2 sentences.
- Exactly 6 FAQ entries.
