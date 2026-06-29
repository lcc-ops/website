---
title: 'ROAS Break-Even Calculator'
description: 'Compute break-even ROAS, target ROAS, and max CPA from your unit price, cost, payment fee and target margin.'
pubDate: 2026-06-30
category: 'ads'
tags: ['roas', 'break-even', 'cpa', 'cpc', 'ads', 'facebook', 'tiktok', 'google']
icon: '📈'
component: 'RoasCalculator'
translationKey: 'roas-calculator'
tldr: 'Break-even ROAS = 1 / (1 − payment% − margin%). A $45 product with 12% COGS, 8% payment fee and 25% target margin needs a break-even ROAS of ~1.85x and target ROAS of ~5.7x.'
faq:
  - q: 'What is a good ROAS for e-commerce?'
    a: 'Break-even is typically 1.5–2.5x. Profitable scaling happens at 3–5x for most Shopify brands. Below 2x, you''re likely losing money once you factor in overhead, returns and refunds. Above 5x, your CPA may be too low relative to category — you''re probably under-spending.'
  - q: 'How do I calculate max CPA?'
    a: 'Max CPA = unit price × (1 − payment fee) − landed cost. That''s the most you can pay per acquisition while still breaking even on the first order. LTV (lifetime value) often justifies 1.3–2.5x this on repeat-purchase products.'
  - q: 'Why is my Facebook ROAS dropping?'
    a: 'Common causes: (1) creative fatigue — same ad shown to same audience too long; (2) audience saturation — CAC creeping up as you exhaust the easy converters; (3) attribution drift — iOS 14.5+ privacy changes under-report iOS conversions; (4) increasing competition raising CPMs. Rotate creatives every 7–14 days and refresh audiences monthly.'
  - q: 'What is a healthy target CPA for dropshipping?'
    a: 'For a $30–50 AOV product, target CPA under $12 is the rule of thumb. Below $8 means you''re likely under-bidding and missing scale; above $15 means your product economics or ad targeting needs work. Use the calculator above for your specific numbers.'
  - q: 'Should I optimize for ROAS or CPA?'
    a: 'Both. ROAS captures the revenue side; CPA captures efficiency. Set a target ROAS (e.g. 3.0x) **and** a target CPA (e.g. $15). If CPA stays under cap but ROAS drops, the algorithm found cheaper conversions on lower-AOV products — investigate. If ROAS is good but CPA caps, you may be hitting creative fatigue.'
  - q: 'How does iOS 14.5 affect ROAS tracking?'
    a: 'Apple''s App Tracking Transparency framework made conversion events from iOS devices underreported by 15–30% for many advertisers. Use Facebook''s Conversions API (server-side) or Google''s Enhanced Conversions to recover attribution. Compare platform-reported ROAS to actual bank-account revenue weekly.'
---

ROAS (Return on Ad Spend) is the **single most-used metric** in paid social, but most sellers eyeball it without checking the math. A 3.0x ROAS sounds great until your margins and fees break it down — at 8% payment fee and 25% target margin, your break-even is closer to 1.85x. Anything below that loses money on the first order.

## How this calculator works

1. **Unit price (USD)** — selling price (post-discount if you run promos).
2. **COGS + shipping (USD)** — landed cost including production, packaging, freight to customer.
3. **Payment fee (%)** — total processor fee including FX and platform commission.
4. **Target margin (%)** — net margin you want after all fixed costs.

The tool returns:

- **Break-even ROAS** = 1 / (1 − payment% − margin%). Below this, every ad dollar loses money.
- **Target ROAS** — multiplier needed to hit your target margin after ad spend.
- **Max CPA** — the most you can pay per acquired customer while staying break-even on order one.

## Beyond ROAS: the levers

ROAS is the output. The input levers are:

- **CTR** (click-through rate) — driven by creative + hook.
- **CVR** (conversion rate) — driven by landing page + offer + price anchoring.
- **AOV** (average order value) — bundles, upsells, threshold shipping.
- **CPM** (cost per thousand impressions) — driven by audience quality and competition.

If ROAS is below target, walk each lever in order: **check CPM** (auction problems?), then **check CTR** (creative fatigue?), then **check CVR** (landing page mismatch?).

## When ROAS lies

- **Attribution windows**: Facebook defaults to 7-day click + 1-day view. Set it explicitly.
- **Brand vs non-brand**: brand search always ROAS-higher because the customer is pre-converted. Compare apples to apples.
- **Cash vs accrual**: you may have paid for a click in May that converted in July. Use the platform's day-of-ad-spend view, not accounting date.

## Tools

- **[Pricing Calculator](/tools/pricing-calculator/)** — model fees into price
- **[FX Withdraw Calculator](/tools/fx-withdraw-calculator/)** — net out FX margin for payout planning
- **Strategy article** — [ROAS formula and target benchmarks](/content/google-ads-roas-formula/)
