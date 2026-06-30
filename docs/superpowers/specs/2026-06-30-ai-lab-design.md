# AI Lab — Design Spec

**Date:** 2026-06-30
**Status:** Draft, awaiting user review
**Scope:** Add an `/ai/` side column to kuajinglab.xyz covering cold-eyed, financially grounded breakdowns of independent AI products and how they make money.

## 1. Background and Positioning

The site today is `kuajinglab.xyz`, a bilingual (en/zh) Astro 5 / Cloudflare Pages static project. It is positioned as a **no-hype, math-first calculator and guide site for cross-border sellers**, with five categories: pricing, shipping, payment, ads, ops. It carries 13 blog posts and 5 calculators.

The user wants to expand the editorial surface to cover **how independent AI products make money** (Cursor, GPT wrappers, solo SaaS, agent studios). This is a different audience angle but a deliberately similar editorial voice: cold, financially literate, no hot takes, no sponsored rankings.

**Positioning decision:** the AI column is a *side project* of the existing site, not a co-equal brand. The site remains primarily about cross-border cost math. The AI column is a clearly labeled "AI Lab" entry next to Home / Content / Tools / Resources / About.

## 2. Goals and Non-Goals

### Goals

- Add a new editorial surface that exercises the same math-first voice the site already has.
- Ship a working landing page, one calculator, and three bilingual articles within one development cycle.
- Preserve existing site SEO and reader experience — no disruption to the cross-border theme.
- Make the new content discoverable: header nav, footer, resources page, about page, search index, RSS, sitemap.

### Non-Goals

- A second brand, second domain, or second design system.
- A second search index, second RSS feed, or second i18n setup.
- AI tools that depend on real-time external APIs (token costs, MRR, stock prices).
- Tutorials on how to *build* AI products. The site writes about *the math* of AI products, not *how to code* them.
- Affiliate / sponsored content. The site already removed the affiliate disclosure in a prior commit.

## 3. Architecture

### Content model

Reuse the existing `content` collection in `src/content.config.ts`. No new collection. Schema is already adequate:

```
title, description, pubDate, category, tags, tldr, faq, draft, translationKey
```

The only novel value used: `category: 'ai'`.

### Routing

| Route | Type | Purpose |
|---|---|---|
| `/ai` | New Astro page | AI Lab landing: intro + 1 calculator card + 3 latest posts |
| `/content/<slug>` | Existing | Article detail (no change) |
| `/content?category=ai` | Existing query | List filtered to AI category (auto-works) |
| `/tools/ai-break-even` | New | New calculator detail page (same template as existing tools) |
| `/tools` | Existing | Tool list (auto-includes new tool) |

### i18n

Append two keys to `src/i18n/ui.ts` for both locales. No removals.

```
nav.ai:    'AI Lab' / 'AI 实验'
category.ai: 'AI monetization' / 'AI 变现'
```

### Header navigation

Add a sixth entry to the `nav` array in `src/components/Header.astro`. The existing `aria-current` logic (`Astro.url.pathname.startsWith(href)`) auto-handles the highlight on `/ai`. No layout change; the existing `gap-6` accommodates six items at desktop width. No mobile hamburger (matches the existing pattern).

### Search index

`scripts/build-search-index.mjs` already walks `src/content/blog/` and `src/content/tools/`. New articles and the new calculator are picked up automatically. No code change.

### RSS / sitemap

`src/pages/rss.xml.ts` uses `getCollection('content')` — auto-includes new articles. `@astrojs/sitemap` auto-includes all prerendered routes including `/ai` and the new article/tool URLs.

### SEO

- Each new page provides `title` and `description` via frontmatter or props.
- The `/ai` landing page passes `alternates: { en: '/ai', zh: '/zh/ai' }` to `BaseLayout` so hreflang tags are generated.
- The 3 articles pair by `translationKey`, generating hreflang automatically.
- Open Graph image: reuse `og-default.svg`. No custom OG for `/ai` (decision: side column does not warrant its own art yet).

## 4. The Calculator — `ai-break-even`

### Fields

| Field | Type | Range | Default | UI label (en) | UI label (zh) |
|---|---|---|---|---|---|
| Monthly price (USD) | number | 1–9999 | 19 | Monthly price | 月费 |
| Customer acquisition cost (USD) | number | 0–9999 | 30 | CAC | 获客成本 |
| Customer lifetime (months) | number | 1–60 | 6 | Avg. lifetime | 平均留存月数 |
| Target payback window (months) | number | 1–36 | 12 | Payback in | 目标回本月数 |

### Outputs (live, recomputed on input)

| Output | Formula | Purpose |
|---|---|---|
| Lifetime value (LTV) | `price × retentionMonths` | Per-customer contribution |
| Payback users | `ceil((cac × retentionMonths) / price)` | How many paid users to break even |
| Monthly MRR target | `paybackUsers × price` | Monthly revenue at the payback point |
| ROI multiple | `ltv / cac` | Health ratio; >1 means customers pay back |

### Why these formulas (SEO content for article 3)

The dominant failure mode in solo AI SaaS is **low ARPU × short retention × high CAC**. A $9/month product with 3-month average lifetime and $40 CAC needs `ceil(40 × 3 / 9) = 14` paid users to break even on acquisition alone, and the customer has already churned by then. The calculator makes this concrete instead of abstract.

### Implementation

- `src/components/tools/AiBreakEvenCalculator.astro`: HTML inputs + client-side `<script>` doing the math, mirroring the structure of `RoasCalculator.astro` and `PricingCalculator.astro`.
- `src/content/tools/ai-break-even/{en,zh}.md`: frontmatter (`title`, `description`, `category: 'pricing'`, `tags: ['ai', 'saas', 'monetization']`, `icon: '🧮'`, `component: 'AiBreakEvenCalculator'`, `translationKey: 'ai-break-even'`, `tldr`, `faq: 4–6 entries`).
- The calculator does **not** call any external API and produces deterministic output. No new dependencies.

## 5. The Three Cold-Start Articles

Each article ships in both `en` and `zh` (linked by `translationKey`). Each carries the full frontmatter schema, with `category: 'ai'`, 4–6 `tags`, a 30–50 char `tldr`, and 4–6 `faq` entries. Each ≤ 1500 words, in the same terse, formula-first voice as the existing cross-border articles.

### Article 1 — Deep case study (Cursor)

- **Slug:** `cursor-business-model`
- **EN title:** *Cursor: How a VS Code Fork Reached $500M ARR Without a Sales Team*
- **ZH title:** *Cursor 商业模型拆解：一个 VS Code 分支如何做到年营收 5 亿而不靠销售*
- **Required content:** pricing tiers; Anysphere corporate structure; revenue back-of-envelope; user count; CAC estimate (community / word-of-mouth); key inflection (Composer / Agent mode); risk factors.
- **Tag sample:** `ai`, `cursor`, `saas`, `case-study`, `monetization`
- **Internal links:** to Article 2 (GPT wrappers patterns), to `ai-break-even` calculator.

### Article 2 — Race breakdown (GPT wrappers)

- **Slug:** `gpt-wrapper-business-models`
- **EN title:** *GPT Wrappers: 8 Patterns That Work, 5 That Burn Cash*
- **ZH title:** *GPT 套壳产品：8 种赚钱套路与 5 种烧钱陷阱*
- **Required content:** a table of common patterns (vertical tool, Copilot augmentation, workflow automation, prompt marketplace, AI customer service, AI image, AI video, AI agent studio) with the typical failure reason for each (weak differentiation, token cost blowup, low retention). A checklist for spotting the burn-cash patterns.
- **Tag sample:** `ai`, `gpt`, `wrappers`, `patterns`, `monetization`
- **Internal links:** to Article 1, to `ai-break-even` calculator.

### Article 3 — Lightweight play + the calculator

- **Slug:** `solo-saas-profit-math`
- **EN title:** *The Math of a $5K/Month Solo AI SaaS*
- **ZH title:** *一个人做到月入 5 万的 AI SaaS 需要多少付费用户*
- **Required content:** lead with the math (LTV / CAC / payback users), embed the `ai-break-even` calculator mid-article ("try your own number"), walk through three typical price points ($9, $29, $99) and show the user count required under realistic CAC and retention assumptions.
- **Tag sample:** `ai`, `saas`, `solo`, `profit`, `math`
- **Internal links:** to Article 1, to Article 2, to `ai-break-even` calculator.

### Inter-article linking

Each article links to at least two other AI Lab surfaces. This builds the internal link graph that supports SEO and keeps the reader on the column.

### Publish cadence

- Article 1 first, then Article 2 three days later, then Article 3 three days later. Spread avoids same-day "content farm" signals.
- `pubDate` set explicitly per article in the frontmatter.
- The implementation plan (next step) decides whether all three articles ship in one batch push or as three sequenced commits. The spec allows either.

## 6. The `/ai` Landing Page

`src/pages/ai.astro`. Structure:

1. **Hero band:** badge "AI Lab", h1 (localized title), subtitle (one sentence about being the math-first AI column), 4 stat chips (3 deep dives / 1 race breakdown / 1 tool / no signup).
2. **Calculator band:** h2 "Calculator", one card pointing to `ai-break-even` with icon, short description, and a "Open calculator" link.
3. **Latest band:** h2 "Latest", 3 cards from `getCollection('content', (e) => !e.data.draft && e.id.endsWith(`/${locale}`) && e.data.category === 'ai')` sorted by `pubDate` desc, sliced to 3.
4. **Why this column band:** 2 short paragraphs — the author runs AI products themselves, the column is a real ledger, not commentary.

The landing reuses existing component patterns: `.badge`, `.card`, `.container-page`, no new design system primitives.

## 7. Light Edits to Existing Pages

### `src/pages/resources.astro` and `src/pages/zh/resources.astro`

Append a 4th section "AI Lab" after the existing "External links" section. The section shows the 3 latest AI articles in the same `.card` grid pattern as the existing "Top reads" section, with a small intro line. Order (Calculators → Top reads → External links → AI Lab) is intentional: AI Lab does not displace the higher-conversion cross-border content.

### `src/pages/about.astro` and `src/pages/zh/about.astro`

Insert a new `sideProject` paragraph between `forSellers` and `principles` in the localized copy object. The `principles` array itself is unchanged. The hero, the intro, the contact line are unchanged.

### `src/pages/index.astro` (home)

No changes. The home page stays focused on cross-border. The AI Lab is reachable via the header nav and the resources page.

## 8. Testing

| Layer | What | How |
|---|---|---|
| Type check | TS / Astro content schemas | `pnpm build` runs `astro check` first |
| Calculator correctness | `ai-break-even` math | One-liner `node -e` against a hand-computed case (LTV=114, payback=10 users, MRR=190, ROI=3.8) |
| Search index | 3 articles + 1 tool present | `node -e 'const d=JSON.parse(require("fs").readFileSync("public/search-index.json")); console.log(d.length, d.filter(x=>x.category==="ai").length)'` |
| UI render | Landing, articles, tool page | `pnpm preview` + browser |
| Search smoke | Queries "ai", "saas", "GPT" return AI results | Browser |
| i18n | English and Chinese text on `/ai`, all 3 articles, the calculator | Browser language switch |
| Header | 6 items, AI Lab `aria-current` on `/ai` | Browser |
| Resources / about | AI Lab section / paragraph visible | Browser |

Test budget: 5–10 minutes for the manual items. Calculator unit case is one node command.

## 9. Build and Deploy

- `pnpm install` — no new dependencies.
- `pnpm build` — `astro check && astro build`, then postbuild (`build-search-index.mjs` + `sync-assetsignore.mjs`).
- `git push` — Cloudflare Pages auto-builds, ~1–2 min to deploy. No Cloudflare dashboard config change required (no KV bindings, no env vars, no Worker route changes).
- After deploy: hard refresh in browser once (`Ctrl+Shift+R`) to defeat any CSS cache.

## 10. Risks and Rollback

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Header too crowded at 6 items | Low | UX slightly worse | Keep `gap-6`; revisit only if real usage data shows it |
| Calculator formula wrong | Low | Misleads user decisions | One unit case + worked example in Article 3 |
| Article facts wrong (revenue, user count) | Medium | Brand trust hit | Every numerical claim must cite a public source (company blog, TechCrunch, The Information, founder interview, PitchBook / Crunchbase public summary). No listicles, no Reddit, no marketing blogs. |
| AI content dilutes main site SEO | Very low | Traffic dispersion | Home page unchanged. AI Lab is a small footprint. |
| `/ai` path collides with future work | Low | Rename cost | Acceptable; the path is human-readable and likely stable. |
| Bilingual quality low | Medium | Reader experience | First pass manual; iterate after reader feedback. |
| Calculator UI labels not translated | Low | Cosmetic | Mirror the i18n pattern used by the other calculators. |

### Rollback

If 7-day post-launch data is clearly negative (no traffic lift, bounce rate up, reader pushback on facts):

1. **Light rollback:** remove the `nav.ai` item from `Header.astro`. The `/ai` URL still works but is not in primary nav. Articles remain indexed.
2. **Heavier rollback:** remove the AI Lab section from `resources.astro`. Move the `ai-break-even` tool card off the resources page. Tool detail page still exists.
3. **Full rollback:** change `category: 'ai'` on the 3 articles to a neutral value, leaving the `/ai` landing empty. **Note:** do not delete the 3 articles or the calculator — they may still drive organic traffic on their own.

Rollback cost: 5 minutes + push. No data migration. The `translationKey` on the 3 articles is preserved in any rollback so the en/zh pairing is not broken.

## 11. File Inventory

### New

```
src/pages/ai.astro
src/content/blog/cursor-business-model/en.md
src/content/blog/cursor-business-model/zh.md
src/content/blog/gpt-wrapper-business-models/en.md
src/content/blog/gpt-wrapper-business-models/zh.md
src/content/blog/solo-saas-profit-math/en.md
src/content/blog/solo-saas-profit-math/zh.md
src/content/tools/ai-break-even/en.md
src/content/tools/ai-break-even/zh.md
src/components/tools/AiBreakEvenCalculator.astro
```

### Modified

```
src/i18n/ui.ts                       (+2 keys: nav.ai, category.ai)
src/components/Header.astro          (+1 nav entry)
src/pages/resources.astro            (+1 section)
src/pages/zh/resources.astro         (+1 section)
src/pages/about.astro                (+1 paragraph in localized copy)
src/pages/zh/about.astro             (+1 paragraph in localized copy)
```

### Unchanged but affected

- `src/content.config.ts` — schema already supports `category: 'ai'`.
- `scripts/build-search-index.mjs` — already scans blog + tools.
- `src/pages/rss.xml.ts` — already iterates all content.
- `@astrojs/sitemap` — already emits all prerendered routes.
- `src/components/BaseHead.astro` — already emits hreflang from alternates.
- `public/search-index.json` — auto-rebuilt by postbuild.

## 12. Open Questions

None at the design level. The implementation plan will surface sequencing questions (which PR first) at writing-plans time.
