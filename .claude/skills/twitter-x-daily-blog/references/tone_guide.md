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
