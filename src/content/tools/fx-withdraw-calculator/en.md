---
title: 'FX & Payout Comparator — PayPal, Wise, Airwallex'
description: 'Compare what you actually receive across PayPal, Wise and Airwallex when converting USD, EUR, GBP or JPY into CNY, USD or EUR.'
pubDate: 2026-06-30
category: 'payment'
tags: ['paypal', 'wise', 'airwallex', 'fx', 'payout', 'currency conversion', 'cross-border']
icon: '💱'
component: 'FxWithdrawCalculator'
translationKey: 'fx-withdraw-calculator'
tldr: 'PayPal embeds a 3–4% FX margin in its conversion rate. Wise charges mid-market rate + 0.41%. Airwallex business accounts undercut both for monthly volume above $50k. On $10,000 USD→CNY, the gap can be $300–800 per transfer.'
faq:
  - q: 'What is the cheapest way to convert USD to CNY as a Chinese seller?'
    a: 'For under $10k/month: Wise Business to a Chinese corporate account (mid-market + 0.41%). For $50k+/month: Airwallex or PingPong Business, both with local-rail settlement and sub-0.5% effective FX. PayPal is the most expensive because its 3–4% FX margin often goes unnoticed.'
  - q: 'Why is PayPal FX margin so high?'
    a: 'PayPal adds 3–4% on top of the mid-market rate and shows the total as a single "conversion fee" on withdrawal. Most sellers see "no fee" on receipt but lose 3% on the implicit rate. Compare the rate PayPal gives you to Google''s "USD to CNY" mid-market rate to see the gap.'
  - q: 'How does Wise make money if its rate is the mid-market?'
    a: 'Wise charges a flat fee on top of mid-market: typically 0.41% for major currencies. A 0.41% margin is far less than the 3–4% PayPal embeds. For $10,000, Wise costs about $41 in fees vs PayPal''s ~$300+ in hidden FX markup.'
  - q: 'Can I receive USD and skip conversion entirely?'
    a: 'Yes. Three paths: (1) open a US business bank account (Mercury, Relay, Brex) and get an ACH routing number — Stripe and Shopify Payments can deposit directly; (2) use Airwallex multi-currency wallet to hold USD, EUR, GBP and pay vendors directly; (3) use Payoneer to receive in local currencies across marketplaces.'
  - q: 'What documents do I need for an Airwallex or Wise account?'
    a: 'Wise Business / Airwallex both require company registration, ID of the beneficial owner, and proof of business activity (website URL, invoices). Approval typically takes 3–7 business days. Personal accounts have looser requirements but lower limits and missing business features.'
  - q: 'Is it safe to leave large balances in Airwallex or Wise?'
    a: 'Wise is FCA-regulated in the UK; client funds are held in safeguarded accounts at tier-1 banks (FSCS protection up to £85k in some cases, but not universally). Airwallex is regulated in Australia, UK, EU, US and Hong Kong. Neither is a bank; balances are not FDIC-insured in the US but are safeguarded in regulated jurisdictions.'
---

Cross-border sellers pay 3–4 different fees when money moves from a customer''s card to a mainland China bank account: **payment processing fee**, **FX margin**, **intermediary bank fee**, **withdrawal fee**. Wise and Airwallex undercut PayPal specifically on FX margin, which is often the single largest leak.

## How this calculator works

1. **Amount** — the gross amount you''re converting.
2. **From currency** — your sales currency (USD most common).
3. **To currency** — typically CNY for Chinese entities, USD for US-based.

The tool returns:

- **FX margin** baked into each provider''s displayed rate.
- **Withdraw fee** (if any).
- **Net receive amount** — what hits your bank.

Defaults assume mid-market reference rates as of writing; your actual rate depends on the day. The **provider with the smallest gap between its fee column and the sum of others** is the winner.

## Common gotchas

- **Intermediary bank fees** (often $15–25 per wire) are not modeled here. Wise and Airwallex both avoid these by using local rails in 60+ countries.
- **Receiving fees**: many providers charge for receiving inbound wires. Stripe, Wise, Airwallex have free receiving for major currencies.
- **Holding balances**: leaving money in a Wise multi-currency wallet gives you mid-market when you transfer between currencies inside the wallet — useful for paying suppliers in EUR while customers pay in USD.

## When to switch

- **Under $10k/month**: Wise Business — best mix of cost, speed (1–2 days) and multi-currency support.
- **$10k–$50k/month**: Airwallex — lower effective rate, prepaid cards, batch payouts.
- **$50k+/month**: Airwallex or PingPong — both offer treasury management and FX hedging on forward contracts.

## Tools

- **[Pricing Calculator](/tools/pricing-calculator/)** — incorporate FX loss into pricing
- **[Fee Comparator](/tools/fee-comparator/)** — compute processor-side fees
- **Strategy article** — [PayPal vs Stripe fees](/content/paypal-vs-stripe-fees/)
