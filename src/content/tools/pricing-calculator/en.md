---
title: 'Product Pricing Calculator for Cross-border Sellers'
description: 'Free Shopify pricing calculator. Enter cost, shipping, fees and target margin — get the suggested price, profit per unit and break-even price instantly.'
pubDate: 2026-06-29
category: 'pricing'
tags: ['pricing', 'shopify', 'calculator', 'profit']
icon: '💰'
component: 'PricingCalculator'
translationKey: 'pricing-calculator'
tldr: 'A cross-border product price equals (cost + shipping + fixed fees) divided by (1 minus commission minus payment fee minus target margin).'
faq:
  - q: 'How do I calculate the right selling price on Shopify?'
    a: 'Use the formula: selling price = (product cost + shipping + fixed fees) ÷ (1 − commission % − payment fee % − target margin %). This calculator does it for you.'
  - q: 'What fees should I include when pricing a product?'
    a: 'At minimum: platform commission, payment processor fee, shipping cost, and any per-order fixed fees (like Shopify''s $0.30 or PayPal''s micro-fee).'
  - q: 'Why is my Shopify profit lower than I expected?'
    a: 'Most sellers forget fixed per-order fees, advertising cost-of-sales, and currency conversion. The break-even price in this calculator assumes 0% margin — anything above it is your profit buffer.'
  - q: 'What is a healthy margin for cross-border ecommerce?'
    a: 'Aim for 25–40% net margin after all fees and shipping. Dropshipping is tighter (15–25%), branded products typically higher (40%+).'
  - q: 'Does this work for Etsy or Amazon?'
    a: 'Yes. Set the commission to Etsy''s 6.5% transaction fee + 3% payment processing, or Amazon''s 15% referral fee. The math is identical.'
---

The **Product Pricing Calculator** answers the question every cross-border seller asks: *what should I charge to actually make money?*

Most pricing formulas stop at "cost × markup." That misses shipping, platform commission, payment processing, and the small per-order fixed fees that quietly eat your margin. This calculator includes all four.

## How to use it

1. Enter your **product cost** (what you pay the supplier, in USD).
2. Add your **shipping cost** per order (or use 0 for free-shipping models).
3. Enter **commission %** (Shopify Payments is 2.9% in the US; Etsy is 6.5% + 3%; Amazon is 15%).
4. Enter **payment processing %** (often the same as commission if your platform bundles it).
5. Add any **fixed per-order fee** (Shopify charges $0.30; PayPal charges $0.49 in some regions).
6. Set your **target net margin** (after all fees).
7. Read the **suggested price**, **break-even price**, and **profit per unit**.

## The formula

```
price = (cost + shipping + fixedFee) / (1 − commission% − payment% − margin%)
```

The break-even price assumes 0% net margin — anything you sell above it is profit.

## Worked example

A $8 product with $3.50 shipping, 2.9% commission, 2.9% payment fee, $0.30 fixed fee, and a 30% target margin:

- Suggested price: **$24.85**
- Break-even price: **$13.05** (zero profit)
- Profit per unit at the suggested price: **$7.46**

If you can't sell above $24.85 in your market, your margin target isn't realistic — either cut costs, raise prices, or accept a thinner margin.

## What this calculator doesn't include

- **Cost of goods sold for returns** (add 5–15% to your cost for typical categories)
- **Advertising cost of sales** (subtract from margin if you run paid traffic)
- **Currency conversion loss** (1–3% if you receive in USD but spend in CNY)

For a full P&L, use the **profit-tracking spreadsheet** in our resources section.

## Common mistakes

| Mistake | Fix |
|---|---|
| Using gross margin instead of net | This calculator uses net margin (after all fees) |
| Forgetting fixed per-order fees | Always add them — they compound at scale |
| Ignoring shipping in the formula | Shipping is a cost, not a marketing line item |
| Mixing currencies | Convert everything to one currency first |

## Reference scenarios (US Shopify defaults)

| Cost | Shipping | Commission | Payment | Fixed | Margin | Suggested | Break-even |
|---|---|---|---|---|---|---|---|
| $5 | $3.50 | 2.9% | 2.9% | $0.30 | 30% | $18.46 | $9.69 |
| $8 | $3.50 | 2.9% | 2.9% | $0.30 | 30% | $24.85 | $13.05 |
| $15 | $5.00 | 2.9% | 2.9% | $0.30 | 25% | $33.16 | $24.87 |
| $40 | $8.00 | 6.5% (Etsy) | 3% | $0.30 | 35% | $98.43 | $63.98 |

Notice how a **2% effective fee increase** (Etsy 6.5% + 3% vs Shopify 2.9% bundled) raises the suggested price ~3.6% on the $40 product — small per unit, large across a catalog.

## When this calculator is not enough

- **Tiered or volume pricing** — B2B or wholesale SKUs need a quantity-break table; this assumes one unit price.
- **Bundle / kit pricing** — component cost allocation is non-trivial; build a separate model.
- **Subscription / recurring** — first-order math is fine, but LTV/CAC math (see ROAS calculator) drives the real margin.
- **Returns-heavy categories** — bake 5–15% return cost into your landed cost before computing price.
- **FX-sensitive supply chains** — if your cost is in CNY and you sell in USD, recompute weekly; the rate alone can swing margin 2–4%.

## Workflow

1. Pull **actual** landed cost (goods + freight + duties) per SKU, not supplier FOB.
2. Add platform commission + payment fee + per-order fixed fee from your storefront contract.
3. Run this calculator at your realistic target margin (start at 25–30%).
4. Cross-check the suggested price against current market on Amazon / Etsy / Shopify search.
5. If suggested price is above market, walk the levers: cost → shipping → fee negotiation → bundle.

## Tools & reading

- **[ROAS Calculator](/tools/roas-calculator/)** — what ad spend can your margin support?
- **[Fee Comparator](/tools/fee-comparator/)** — set the right payment fee assumption
- **[CBM Calculator](/tools/cbm-calculator/)** — model freight accurately per SKU
- **Strategy article** — [Pricing formula explained](/content/pricing-formula-explained/)