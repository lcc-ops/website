---
title: "9 people, 10M USD year-one to 100M USD year-three: how Wesley Tian's AI-headshot shop slices a 200 USD studio visit into a 10–30 USD software product"
description: "A case profiles Wesley Tian's AI-headshot product: 9 employees, 4 months to 1M USD/year, 2 years to 10M USD/year, 1M+ professionals served, 25M+ headshots generated. Pricing: 10–30 USD per set vs the 200 USD+ studio alternative. The interesting part is not 'AI generates headshots' — it is the vertical-niche slicing by profession (lawyer, realtor, doctor, founder, LinkedIn). The unit economics per profession, the per-job CAC math, and the four gaps the case does not cover, below."
pubDate: 2026-07-10
category: 'ai'
tags: ['ai', 'headshot', 'professional-services', 'vertical-niche', 'case-study', 'monetization']
translationKey: 'x-wesley-tian-headshot-9ppl'
tldr: "An AI-headshot product hits 1M USD/year in 4 months, 10M USD/year in 2 years, with 9 employees and 1M+ served. Pricing 10–30 USD vs the 200 USD+ studio alternative. The interesting part is not 'AI generates photos' — it is the vertical-niche slicing by profession. Each profession gets its own landing page, its own pricing anchor, and its own repeat-purchase triggers. The unit economics per profession and the four gaps the case does not cover, below."
faq:
  - q: "What does the case actually document?"
    a: "An AI-headshot product that turns a few selfies into a studio-grade professional headshot. 9 employees. 4 months to 1M USD/year. 2 years to 10M USD/year. 1M+ professionals served. 25M+ headshots generated. Average per-user generated 25 headshots — meaning repeat purchases are the load-bearing revenue driver. The product sells at 10–30 USD per set, against the 200 USD+ studio alternative."
  - q: "What is the unit economics?"
    a: "Per generation: GPT / Claude prompt pass (10 sec), selfie-to-headshot AI model (60–90 sec), background swap (15 sec), user selection (5 min). Server cost per generation roughly 0.05–0.20 USD at GPT-image / Stable Diffusion scale. Selling price 10–30 USD. Per-generation gross margin 90%+ at the marginal level. Fixed cost: 9 employees (engineers, designers, marketing, ops). Per-employee revenue at 10M USD/year run rate is 1.1M USD/year — top decile for a 9-person SaaS / consumer-product team."
  - q: "Why does vertical-niche slicing matter?"
    a: "Three reasons. (1) Landing-page conversion: a lawyer-targeted page with lawyer-specific copy converts 3–5x better than a generic 'AI headshot for everyone' page. (2) Pricing anchor: the lawyer page anchors against the 200 USD+ studio alternative; the generic page anchors against the 9.99 USD mass-market photo tool. (3) Repeat purchase: each profession has its own trigger (job change, industry switch, resume refresh, holiday) — 25 headshots per user across 4–6 professions over 3 years is the design."
  - q: "What is the per-profession math?"
    a: "Lawyer: 200 USD+ studio vs 10–30 USD software. ~1M lawyers in the US. At 1% market penetration × 25 headshots per user × 15 USD average = 3.75M USD TAM per vertical per year. Realtor: similar. Doctor: similar but smaller pool. Founder: smaller pool, higher willingness-to-pay. LinkedIn-only: 1B+ users, but lower WTP. The case implies the operator is monetizing 4–6 of these slices in parallel."
  - q: "What is the risk?"
    a: "Four risks. (1) Model commoditization — as GPT-image, Stable Diffusion, and open-source face-preservation models improve, the technical moat erodes. (2) Trust erosion — privacy and biometric-data regulation is tightening; a 2026 breach or regulatory action hits all slices at once. (3) Studio response — traditional photography studios ship their own AI features; their brand and existing customer base beat the AI-product's marketing. (4) Per-profession saturation — once a niche is well-served by 2–3 competitors, the CAC climbs and the per-user repeat-purchase rate drops."
  - q: "What does the case skip?"
    a: "Four gaps. (1) Per-profession revenue split is not disclosed — the 10M USD/year aggregate hides which slice carries the load. A 80% lawyer + 20% everything-else split is very different from a balanced split. (2) Refund rate on AI headshots is high in the category (15–25% — 'doesn't look like me', 'face is wrong', 'lighting bad'); the case does not break this out. (3) Customer-support load — each refund request requires manual review by a designer or trained operator; the 9-person team capacity here is the bottleneck. (4) Per-acquisition cost by landing page is not shown — lawyer-CAC and realtor-CAC are very different."
---

A case profiles Wesley Tian's AI-headshot product. 9 employees. 4 months to 1M USD/year. 2 years to 10M USD/year. 1M+ professionals served. 25M+ headshots generated. Average per-user 25 headshots — repeat purchases are the load-bearing revenue. Pricing 10–30 USD vs the 200 USD+ studio alternative. The interesting part is not 'AI generates photos' — it is the vertical-niche slicing by profession. Each profession gets its own landing page, its own pricing anchor, its own repeat-purchase triggers. The unit economics per profession and the four gaps the case does not cover, below.

## The vertical-niche slicing math

```
Per profession:
  Lawyer:        ~1M in US, 200 USD+ studio anchor, 15 USD avg
                1% penetration × 25 headshots × 15 USD = 3.75M USD TAM/yr
  Realtor:       ~1.5M in US, similar math                  ≈ 5M USD TAM/yr
  Doctor:        ~1M in US, smaller pool, similar math      ≈ 3M USD TAM/yr
  Founder:       smaller pool, higher WTP                   ≈ 1–2M USD TAM/yr
  LinkedIn-only: 1B+ users, lower WTP                       large but low-margin

The case implies 4–6 slices monetized in parallel.
10M USD/year aggregate at 9 employees ≈ 1.1M USD / employee
```

The interesting core move is the slicing. A generic 'AI headshot for everyone' product lands in the 9.99 USD mass-market bucket and competes on price. A profession-targeted product lands in the 30 USD bucket and competes on conversion-to-studio-alternative. The per-user revenue is 3x, the conversion rate is 3–5x, and the CAC payback is faster.

## The unit economics per generation

```
Per generation:
  Prompt + selfie ingestion:       10 sec
  Selfie-to-headshot model:        60–90 sec
  Background swap:                 15 sec
  User selection + download:       5 min

Server cost:                      0.05–0.20 USD per generation
Selling price:                    10–30 USD
Marginal gross margin:            90%+

Fixed cost:
  9 employees (eng, design, marketing, ops)
  At 10M USD/year run rate:       1.1M USD / employee
```

The 9-person team is the bottleneck, not the model cost. Each employee is generating roughly 1.1M USD/year in revenue — top-decile productivity for a consumer-product team. The model cost is the variable; the team cost is the fixed.

## Why 25 headshots per user

The repeat-purchase number (25 headshots per user) is the design, not an accident. Each profession has its own trigger:

- Lawyer changes jobs → new headshot needed.
- Realtor rebrands brokerage → new headshot.
- Doctor moves practice → new headshot.
- Founder changes startup → new headshot.
- LinkedIn profile refresh every 2–3 years → new headshot.

The product is engineered to be re-purchased 4–6 times across 3–4 professions over a 3-year user lifecycle. The 25 headshots per user is the cumulative output of that cycle, not the per-engagement count.

## What this case does not cover

- **Per-profession revenue split.** The 10M USD/year aggregate hides which slice carries the load. An 80% lawyer + 20% everything-else split is very different from a balanced split. The unit economics, CAC, and refund rate differ by profession.
- **Refund rate.** AI-headshot products in the category see 15–25% refund rates — 'doesn't look like me', 'face is wrong', 'lighting bad'. The case does not break this out. A 20% refund rate cuts gross margin from 90% to 70%.
- **Customer-support load.** Each refund requires manual review by a designer or trained operator. The 9-person team capacity here is the bottleneck. A scaling spike without support automation hits the team directly.
- **Per-acquisition cost by landing page.** Lawyer-CAC and realtor-CAC are very different. The case does not show whether one slice is acquiring customers at 5 USD CAC and another at 50 USD CAC.

## Bottom line

The model is real: 1M USD/year in 4 months, 10M USD/year in 2 years, 9 employees. The vertical-niche slicing is the core move that lifts the product out of the 9.99 USD mass-market bucket into the 30 USD per-profession bucket. Repeat purchases (25 headshots per user across 4–6 professions) carry the load. A reader replicating the playbook should pick 1 profession first, anchor the pricing against the studio alternative, and engineer for 4–6 repeat purchases per user over 3 years. Treat the 10M USD/year as the realistic steady-state at 9 employees; scaling past 20M USD/year requires more employees or process automation.