# AI Lab blog post schema

Required YAML frontmatter (matches the existing 8 AI Lab posts):

```yaml
---
title: 'A single-quoted headline (apostrophe escapes for em-dashes)'
description: 'A single-sentence subtitle. 80-160 chars. Math-driven when possible.'
pubDate: YYYY-MM-DD
category: 'ai'
tags: ['ai', '<niche>', 'case-study', 'monetization']
translationKey: '<slug>'
tldr: 'A 1-2 sentence summary. Plain language. No hype.'
faq:
  - q: 'Question 1?'
    a: 'Answer 1. Math / source citation when relevant.'
  - q: 'Question 2?'
    a: 'Answer 2.'
  - q: 'Question 3?'
    a: 'Answer 3.'
  - q: 'Question 4?'
    a: 'Answer 4.'
  - q: 'Question 5?'
    a: 'Answer 5.'
  - q: 'Question 6?'
    a: 'Answer 6.'
---

# Markdown body

The body must contain, in this order:

1. One paragraph of context.
2. A section heading (##) with a numeric or comparative table.
3. A section on the cost structure or unit economics.
4. A section on what the **case** (NOT "the post" — see tone_guide.md) does
   NOT cover (limits, failures, gaps).
5. A "Take-away" or "Conclusion" section.

**There is no source footer.** Do NOT add a `**Source**: linked from...`
block at the bottom. The case reads as if the writer is documenting
a model directly. Provenance lives only in `scripts/scrapers/data/zsxq.sqlite3`.

Length: 1500-2200 words. Both `en.md` and `zh.md` should match in length.

## Naming

| Field | Rule |
|---|---|
| `slug` (folder name) | kebab-case, lowercase, 3-6 words, no numbers at start, e.g. `etsy-ai-digital-products` |
| `translationKey` | Identical to `slug` |
| `title` (en) | Sentence case (only first word + proper nouns capitalized) |
| `title` (zh) | No specific case, mark a 12-30 字 punchy title |
| `pubDate` | Today's UTC date in YYYY-MM-DD format |
| `tags` | Always includes 'ai', 'case-study', 'monetization'. Add 1-2 niche tags. |
