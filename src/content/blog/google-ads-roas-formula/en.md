---
title: 'Google Ads ROAS Formula: The Real Break-even Calculation'
description: 'How to calculate Google Ads ROAS, break-even ROAS, and target ROAS based on your actual margin. Includes formula, calculator, and common ROAS mistakes.'
pubDate: 2026-06-30
category: 'ads'
tags: ['google-ads', 'roas', 'roi', 'break-even']
translationKey: 'google-ads-roas-formula'
tldr: 'ROAS = revenue ÷ ad spend. Break-even ROAS = 1 ÷ net margin (as a decimal). A 30% net margin store needs 3.33× ROAS to break even on ad spend alone.'
faq:
  - q: 'What is a good ROAS for Google Ads?'
    a: 'It depends on your net margin. Break-even ROAS = 1 ÷ net margin. So a 25% net margin store needs 4× ROAS to break even; anything above is profitable. Most ecommerce stores target 3–6× ROAS.'
  - q: 'How is ROAS different from ROI?'
    a: 'ROAS measures ad revenue vs ad spend only. ROI includes all costs (COGS, shipping, fees, overhead). ROAS of 5× might be unprofitable if your margin is under 20%.'
  - q: 'What ROAS is needed for a 20% net margin?'
    a: 'Break-even ROAS = 1 ÷ 0.20 = 5×. Target ROAS = 5 × 1.5 = 7.5× for a 50% profit buffer on ad spend.'
  - q: 'Does Google Ads report ROAS the same way I calculate it?'
    a: 'Google reports "conversion value" ROAS, which uses the value you pass back at conversion (often the order total minus shipping). Your calculation may differ if you include lifetime value or exclude refunds.'
  - q: 'How do I improve low ROAS?'
    a: 'Improve Quality Score (better ads, landing pages), tighten audience targeting, raise bids on winners, cut losers, and improve store-side conversion rate. A 1% conversion rate improvement often moves ROAS by 20%+.'
---

ROAS is the most quoted metric in ecommerce. Most sellers don't calculate it correctly — and end up celebrating unprofitable campaigns.

## What ROAS actually measures

```
ROAS = revenue from ads ÷ ad spend
```

A ROAS of 4× means every $1 in ad spend returned $4 in revenue. That's the gross number. It tells you nothing about whether you made money.

## The break-even formula

```
Break-even ROAS = 1 ÷ net margin (as decimal)
```

Where **net margin** = profit after all costs (COGS, shipping, fees, refunds) divided by revenue.

For a 25% net margin store: 1 ÷ 0.25 = **4× break-even ROAS**.

Anything above 4× is profit on ad spend alone. Anything below is loss.

## Worked example

A store with these unit economics:
- Sale price: $50
- Cost: $12
- Shipping: $4
- Payment + platform fees: $3 (6%)
- **Net profit per sale: $31 (62% margin)**

Break-even ROAS = 1 ÷ 0.62 = **1.61×**

If the store achieves 3× ROAS, profit per sale attributed to ads:
```
Ad-driven revenue: $50
Ad spend allocation: $50 ÷ 3 = $16.67
Net profit: $50 − $16.67 − $12 − $4 − $3 = $14.33
```

3× ROAS looks great but the actual margin on ad-driven sales is 28.7%, not 62%. The ad cost is real money you spent.

## Target ROAS with profit buffer

Don't aim for break-even. Add a buffer for other costs:

| Scenario | Target ROAS at 25% net margin |
|---|---|
| Break-even | 4× |
| 25% profit buffer | 5.33× |
| 50% profit buffer | 8× |
| 100% profit buffer (double profit) | 16× |

For most stores, target **2× break-even ROAS** as a starting point. Cut campaigns that fall below break-even for 2+ weeks.

## Common ROAS mistakes

### 1. Confusing gross and net margin

A 50% gross margin product (cost = 50% of price) might have a 20% net margin after fees, shipping, and returns. Using 50% in the formula gives a break-even of 2× when you actually need 5×.

### 2. Ignoring returns and chargebacks

Apparel stores with 15% returns need to add ~10% to cost. If your "ROAS" calculation ignores returns, you're lying to yourself.

### 3. Not subtracting payment processing

$100 in revenue isn't $100 to you. Stripe takes $3.20. Factor it in.

### 4. Counting assisted conversions wrong

Google's "conversion value" includes view-through conversions and cross-device. A customer who saw your ad on mobile but bought on desktop after a Google search is still counted. This inflates ROAS by 10–30%.

### 5. Lifetime value blind

A first purchase at break-even ROAS might be fine if LTV is 3× the first order. But if LTV is identical to AOV, you need first-order profitability.

### 6. Reporting time window

ROAS reported at 24 hours looks very different from 30-day ROAS. Most platforms let you pick. For cold-traffic campaigns, use 7-day or longer windows.

## ROAS by industry benchmark (US ecommerce 2026)

| Category | Median ROAS | Top quartile |
|---|---|---|
| Apparel | 2.8× | 5× |
| Electronics | 3.5× | 6× |
| Home goods | 3.2× | 5.5× |
| Beauty | 4× | 7× |
| Supplements | 3.8× | 6.5× |
| Pet | 4.5× | 7.5× |
| Digital products | 6× | 12× |

These are aggregate numbers. Your store's break-even is the only number that matters for your decision.

## How to improve ROAS without raising prices

1. **Quality Score** — better ads, more relevant landing pages. Each Quality Score point typically reduces CPC by 10–15%.
2. **Audience segmentation** — separate high-intent search from broad display. Search ROAS is 3–5× display ROAS.
3. **Negative keywords** — add them weekly. Most wasted spend comes from irrelevant queries.
4. **Ad schedule bid adjustments** — cut bids 30%+ on hours/days with low conversion rates.
5. **Device bid adjustments** — mobile often converts at half the rate of desktop. Bid accordingly.
6. **Landing page A/B test** — a 1% conversion improvement on a 2% page is a 50% lift in revenue per visitor.

## When to accept low ROAS

- **New customer acquisition**: First-order ROAS of 1× is fine if LTV is 3×. Track repeat purchase rate.
- **Brand defense**: Bidding on your own brand name at low ROAS protects against competitors.
- **List building**: Email subscribers often have 5–10× LTV of paid customers. Accept low ROAS on lead-gen.

## Try the math

Use our [Product Pricing Calculator](/tools/pricing-calculator/) to model how ad cost affects your target margin.