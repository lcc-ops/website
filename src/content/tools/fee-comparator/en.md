---
title: 'PayPal vs Stripe Fee Comparator'
description: 'Compare monthly PayPal and Stripe processing fees for your unit price and order volume. See which is cheaper.'
pubDate: 2026-06-30
category: 'payment'
tags: ['paypal', 'stripe', 'fees', 'comparison', 'payments', 'e-commerce']
icon: '💳'
component: 'FeeComparator'
translationKey: 'fee-comparator'
tldr: 'Both charge ~3% + $0.30 on standard card transactions, but rates and fixed fees differ per region and card type. Stripe is usually 1–2% cheaper on cross-border card volume because PayPal adds a fixed-fee layer and currency-conversion margin.'
faq:
  - q: 'Who is cheaper for cross-border e-commerce, PayPal or Stripe?'
    a: 'For direct card payments Stripe is usually 1–2% cheaper on cross-border volume. PayPal adds a 1.5% international fee plus a 3–4% FX margin when settling to a non-USD currency. Stripe''s standard international card fee is 1.5% plus 2%, while Adyen (Stripe competitor) can be lower still at volume.'
  - q: 'What is the cheapest payment processor for Shopify?'
    a: 'Shopify Payments (powered by Stripe) is typically the cheapest because Shopify absorbs part of the processing fee at higher plans. Outside Shopify, Stripe''s standard 2.9% + $0.30 is competitive. PayPal Payflow Pro charges an additional $0.10 per transaction on top of PayPal rates.'
  - q: 'How do I avoid chargebacks on PayPal and Stripe?'
    a: 'Both offer 3D Secure (3DS) verification. Enable it everywhere. Stripe Radar (free with Stripe) blocks suspect cards using ML; PayPal''s Seller Protection covers fraud claims if you ship to the verified address and provide tracking. See [Chargeback Prevention](/content/payment-chargeback-prevention/) for the full playbook.'
  - q: 'Does PayPal have a fixed monthly fee?'
    a: 'No monthly fee on standard commercial accounts. PayPal charges 4.4% + $0.30 per domestic commercial transaction, plus 1.5% international, plus a 3–4% FX margin if you withdraw in a different currency than the sale. Micropayments account (under $10) has a separate rate: 5% + $0.05.'
  - q: 'How does Stripe handle currency conversion?'
    a: 'Stripe charges in the customer''s currency and converts to your settlement currency at the interbank rate plus 1%. If you want to receive the original currency, enable multi-currency settlement — Stripe will hold balances in USD, EUR, GBP, JPY and others at no fee.'
  - q: 'Can I use both PayPal and Stripe at the same time?'
    a: 'Yes. Most ecommerce platforms (Shopify, WooCommerce, BigCommerce) support both. Test both methods against your checkout conversion: some buyer segments (older EU consumers, B2B buyers) strongly prefer PayPal or even bank transfer, while younger / mobile-first customers prefer wallets.'
---

Both PayPal and Stripe charge roughly **3% + $0.30** on standard card transactions, but the structures diverge quickly once you add international cards, currency conversion, and dispute fees. A $35 product on 300 orders/month generates $10,500 in revenue — a 1% effective-rate difference is $1,260/year.

## How this calculator works

1. **Unit price (USD)** — average order value.
2. **Monthly volume** — total orders per month.

The tool returns:

- **Monthly fee** for each provider
- **Effective rate** = monthly fee ÷ monthly revenue
- **Wins by** — the dollar gap per month

Defaults assume **PayPal commercial transactions** (4.4% + $0.30) and **Stripe standard card** (2.9% + $0.30 base, with an estimated 1.5% cross-border card surcharge baked into Stripe's effective rate for international orders). Adjust the inputs to your actual mix.

## Effective fee across order volumes

| Unit price | Monthly orders | Revenue | PayPal fee | Stripe fee | Gap / month | Gap / year |
|---|---|---|---|---|---|---|
| $25 | 200 | $5,000 | $280 | $194 | $86 | $1,032 |
| $35 | 300 | $10,500 | $569 | $404 | $165 | $1,980 |
| $60 | 500 | $30,000 | $1,590 | $1,140 | $450 | $5,400 |
| $120 | 150 | $18,000 | $948 | $696 | $252 | $3,024 |

The gap scales **roughly linearly with revenue**, not with order count. At $30k/month, PayPal's premium is ~$5,400/year — that's a full-time employee in some markets. Stripe wins on standard domestic card volume; PayPal wins only when buyers specifically refuse to pay by card.

## What's NOT in this calculator

- **Chargeback / dispute fees** ($15–20 per case) — plan a reserve.
- **Subscription billing discounts** — Stripe Billing and PayPal Subscriptions have different retained-rate cards.
- **Local methods** (iDEAL, Klarna, Alipay) — providers like Adyen, Mollie, Airwallex Payment Acceptance aggregate these with one fee.
- **Card-present vs card-not-present** — keyed and online transactions price differently from POS.

## Common mistakes

- **Reading "no monthly fee" as free** — PayPal has no monthly fee but a higher per-transaction rate. Run the math.
- **Ignoring the 1.5% international surcharge** — it stacks on top of the base rate. A 4.4% + 1.5% PayPal cross-border transaction costs 5.9% before FX.
- **Forgetting currency conversion** — if your customer pays in EUR and you settle in USD, PayPal takes 3–4% on top of the displayed rate. Stripe is 1%.
- **Underestimating chargebacks** — budget 0.1–0.3% of revenue as a reserve; for high-AOV niches (electronics, supplements) it can hit 1%.

## When to switch providers

- **You're under $50k/month** and primarily domestic: PayPal's check is rare; Stripe tends to be 0.5–1% cheaper.
- **You sell across borders**: Stripe's interbank FX is 1–2% cheaper than PayPal's embedded margin.
- **You have B2B or older EU customers**: keep PayPal as a secondary option even if Stripe is primary — conversion often increases.
- **You sell subscriptions**: Stripe Billing's retained card rate is materially lower than PayPal Subscriptions at scale.
- **You want local methods** (iDEAL, Bancontact, BLIK): Adyen or Mollie, not PayPal/Stripe direct.

## When this calculator is not enough

- **Volume-tiered pricing** kicks in at $100k+/month — contact both for custom rates; this calculator assumes posted rates.
- **Marketplace-specific fees** (Etsy Payments, Amazon Seller Central) have their own rate cards.
- **Crypto or BNPL** (Klarna, Afterpay) sit outside both PayPal and Stripe's standard pricing.

## Workflow

1. Pull your last 90 days of revenue and order count from your storefront.
2. Run this calculator with **actual** unit price (median, not list).
3. Cross-check the gap with the **Effective Fee** table above for your revenue band.
4. If switching, run a 30-day A/B test on Stripe Checkout before migrating fully.

## Tools & reading

- **[Pricing Calculator](/tools/pricing-calculator/)** — feed the effective rate back into your margin
- **[FX Withdraw Calculator](/tools/fx-withdraw-calculator/)** — measure post-fee receive amount for payouts
- **[ROAS Calculator](/tools/roas-calculator/)** — fold the effective rate into break-even ad math
- **Strategy article** — [PayPal vs Stripe fees deep dive](/content/paypal-vs-stripe-fees/)