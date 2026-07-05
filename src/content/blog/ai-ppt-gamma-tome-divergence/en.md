---
title: 'Why Gamma hit 100M USD ARR and Tome shut down in the same AI-PPT race'
description: 'Two AI-PPT products, one outcome of 100M USD ARR with 100 people at 2.1B USD valuation, the other shut down in April 2025 despite 32M USD raised. The split is a product-intuition story, not a model-performance story. Cold read of the numbers and what a solo builder can take from it.'
pubDate: 2026-07-06
category: 'ai'
tags: ['ai', 'ppt', 'product-strategy', 'case-study', 'monetization', 'open-source']
translationKey: 'ai-ppt-gamma-tome-divergence'
tldr: 'Gamma reportedly hit 100M USD ARR by end-2025 with fewer than 100 people and a 2.1B USD valuation. Tome shut its product down on 30 April 2025 after raising 32M USD. Both targeted the same AI-PPT job. The gap is not the model — both used roughly equivalent third-party LLMs. The gap is what the user actually came to do: format a slide, not think about content. The takeaway for a solo builder is to compete against "user opens PowerPoint" rather than against Gamma, and to pick a vertical slice where a 9.9 USD/month price converts at 1,000 paying users.'
faq:
  - q: "What are the two anchor numbers?"
    a: 'Gamma: launched 2022, 70M users by end-2025, 100M USD ARR by end-2025, valuation 2.1B USD, fewer than 100 employees. Tome: raised 32M USD, shut its product down on 30 April 2025. The contrast is in the same niche, in the same calendar window.'
  - q: "Why did Tome fail?"
    a: 'The case is blunt. Tome positioned itself as "AI helps you think about the slide content". Users came to format a deck they already had in their head, not to brainstorm what to put on it. The mental model mismatch meant low frequency-of-use and high churn. A product that runs once a month does not retain against a product that runs weekly.'
  - q: "Why did Gamma work?"
    a: 'Gamma positioned itself as "AI handles layout and styling; you type the content". The user provides the words; the AI handles everything else. This matches the underlying job — "I know what to say, I do not want to spend two hours formatting it" — and gets the user into a weekly cadence. Weekly use is the load-bearing frequency that supports 20 USD/month pricing.'
  - q: "What is the open-source entry point for a solo builder?"
    a: 'PptxGenJS, a JavaScript library that generates standard .pptx files. ~5,000 GitHub stars, ~1.27M weekly downloads. The library handles the file-format plumbing (layouts, masters, themes, animations). The AI layer wraps it: user types a prompt, the system generates an HTML-styled deck, exports to .pptx. The library is the part you do not have to build.'
  - q: "What are the three viable solo paths?"
    a: 'A: Vertical-scoped tool — "AI weekly report deck", "AI investor BP", "AI training slides". Narrower than Gamma, so the AI quality bar is lower and the conversion is higher. Target 9.9 USD/month × 1,000 paying users = ~120k USD/year. B: Templates-plus-AI-fill — sell templates on Gumroad at 29 USD each, layer an AI-fill subscription on top. Templates and subscription stack. C: Custom automation for enterprises that produce weekly reports — data source plus template plus AI polish, priced 500–2,000 USD/month per client. Ten clients is a viable solo business.'
  - q: "What does the case leave out?"
    a: 'Three gaps: (1) gross margin on Gamma at 100M USD ARR — the cost of LLM tokens and storage at 70M users is not named, and could be 15–25% of revenue; (2) the retention curve on Gamma — does the weekly cadence hold at year two, or does novelty decay and the product become a quarterly-use tool? (3) the underlying moat — Gamma has none of the traditional SaaS moats (no network effect, no switching cost, no proprietary data); the moat is execution speed and brand. The case is silent on whether that moat compounds or erodes.'
---
Two AI-PPT products competed in the same window. One hit 100M USD ARR with under 100 people at a 2.1B USD valuation. The other shut down in April 2025 after raising 32M USD. Below is a cold read of why one worked and the other did not, plus a checklist for a solo builder looking at the same niche.

## The two numbers

| Company | Outcome | Window | Capital | Headcount |
|---|---|---|---|---|
| Gamma | 100M USD ARR, 2.1B USD valuation | Launch 2022, ARR target end-2025 | Not named | <100 |
| Tome | Product shut down | 30 April 2025 | 32M USD raised | Not named |

The contrast is the entire case. Same niche. Same calendar window. Different outcomes by an order of magnitude on revenue and a full wipe on the loser side.

## What Gamma actually sells

The case is direct: Gamma sells layout and styling, not content. The user types the words. Gamma handles the slide structure, the visual rhythm, the image placement, and the export. The job-to-be-done is "I know what I want to say, I do not want to spend two hours saying it in PowerPoint".

This positioning drives a weekly cadence. People who make decks weekly (consultants, founders, PMs, sales engineers, internal comms people) come back. Weekly use supports 20 USD/month pricing because the cost-per-use is roughly 50 cents.

The acquisition cost matters because retention is the load-bearing number. The case does not give Gamma's CAC, but at 70M users and 100M USD ARR, the implied ARPU is around 1.4 USD/year — which means Gamma is pricing on a freemium-to-paid-conversion model, not on a per-paid-seat model. The "users" headline is mostly free.

## What Tome sold

Tome positioned itself as "AI helps you think about what goes on the slide". The user types a topic, the AI proposes an outline, the user edits, the AI formats.

The mental model mismatch is the entire failure mode. People who came to Tome already had a slide outline in their head — that is why they opened a slide tool. The AI's "what should I say" suggestion was at best redundant, at worst annoying. The product got used once, the user left, and Tome never built the weekly cadence Gamma built.

The lesson is not that AI cannot help with content ideation. The lesson is that the buyer of an AI-PPT tool is not buying content ideation. They are buying "format this for me". When the product does something else, the user leaves.

## The solo-builder entry point

The case names a specific open-source substrate: PptxGenJS. A JavaScript library that generates standard .pptx files, ~5,000 GitHub stars, ~1.27M weekly npm downloads. The library handles the file-format layer: layouts, masters, themes, animations, the boring plumbing that takes a year to build from scratch.

The AI layer sits on top: user types a prompt, the system generates HTML-styled slides, exports to .pptx. Recent updates added PPT animation support. The case mentions an X post where this combo hit 50k impressions, 400 likes, 350 bookmarks, 100+ comments — and the comments were entirely "how do I use this", "can you share it". Demand signal is real.

Three viable solo paths the case names:

1. **Vertical-scoped tool.** "AI weekly report deck". "AI investor BP". "AI training slides". Narrower than Gamma, so the AI quality bar is lower and the conversion rate is higher. Target 9.9 USD/month × 1,000 paying users ≈ 120k USD/year. The 9.9 number is below Gamma's 20 USD and above the "free ChatGPT" floor, which is the price band where willingness-to-pay has been validated.
2. **Templates-plus-AI-fill.** Sell templates on Gumroad at 29 USD each (this alone is a real business for many creators). Layer an AI-fill subscription on top so the template fills itself when the user pastes their content. Templates and subscription stack as two revenue lines.
3. **Custom automation for enterprises with weekly report decks.** Data source plus template plus AI polish, priced 500–2,000 USD/month per client. Ten clients is a viable solo business at six figures. The sales cycle is longer but the retention is structural.

The unifying frame the case gives is the one to remember: a solo builder in this niche is not competing against Gamma. A solo builder is competing against "user opens PowerPoint". As long as the product is meaningfully faster than manual formatting, there is a paying user.

## What this case does not cover

The case is clear on the product-intuition difference. It is silent on the three points that decide whether a Gamma-style business can be built solo:

1. **Gamma's gross margin at scale.** At 70M users and 100M USD ARR, the implied free-to-paid conversion is single-digit percent. The cost of LLM tokens and storage for 70M free-tier users is not named and could be 15–25% of revenue — a meaningful drag on margin compared with traditional SaaS.
2. **Retention curve.** Does the weekly cadence hold at year two? Novelty decay is the standard failure mode for AI content tools. If Gamma decays to monthly use, the 20 USD/month pricing no longer holds and the unit economics flip.
3. **The moat.** Gamma has none of the traditional SaaS moats (no network effect, no switching cost, no proprietary data). The moat is execution speed and brand. The case does not say whether that moat compounds or erodes. If a serious competitor launches in mid-2026 with a faster model and the same positioning, can Gamma hold its conversion curve?

The product-intuition lesson is real and portable. The unit-economics question is the one to come back to.