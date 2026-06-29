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

## What's NOT in this calculator

- **Chargeback / dispute fees** ($15–20 per case) — plan a reserve.
- **Subscription billing discounts** — Stripe Billing and PayPal Subscriptions have different retained-rate cards.
- **Local methods** (iDEAL, Klarna, Alipay) — providers like Adyen, Mollie, Airwallex Payment Acceptance aggregate these with one fee.

## When to switch providers

- **You're under $50k/month** and primarily domestic: PayPal's check is rare; Stripe tends to be 0.5–1% cheaper.
- **You sell across borders**: Stripe's interbank FX is 1–2% cheaper than PayPal's embedded margin.
- **You have B2B or older EU customers**: keep PayPal as a secondary option even if Stripe is primary — conversion often increases.

## Tools

- **[Pricing Calculator](/tools/pricing-calculator/)** — feed the effective rate back into your margin
- **[FX Withdraw Calculator](/tools/fx-withdraw-calculator/)** — measure post-fee receive amount for payouts
- **Strategy article** — [PayPal vs Stripe fees deep dive](/content/paypal-vs-stripe-fees/)
