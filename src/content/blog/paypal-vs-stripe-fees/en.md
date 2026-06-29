---
title: 'PayPal vs Stripe Fees in 2026: The Real Cost Per Sale'
description: 'Side-by-side fee comparison of PayPal and Stripe for cross-border sellers. Includes micro-fee trap, chargeback handling, and currency conversion costs.'
pubDate: 2026-06-29
category: 'payment'
tags: ['paypal', 'stripe', 'fees', 'comparison']
translationKey: 'paypal-vs-stripe-fees'
tldr: 'Both PayPal and Stripe charge 2.9% + $0.30 for US cards. PayPal adds 1.5% for international cards and 3–4% for currency conversion; Stripe charges 1% extra for international and uses wholesale FX rates.'
faq:
  - q: 'Which is cheaper, PayPal or Stripe?'
    a: 'For US-domestic cards, they''re identical (2.9% + $0.30). For international cards, Stripe is usually 0.5–1% cheaper. For currency conversion, Stripe is 1–3% cheaper.'
  - q: 'Does PayPal charge a monthly fee?'
    a: 'No monthly fee for standard PayPal business accounts. PayPal Pro, Payments Pro, and PayFlow are discontinued or being sunset in favor of PayPal Checkout (no monthly fee).'
  - q: 'Can I use both PayPal and Stripe on Shopify?'
    a: 'Yes — but if you use Stripe (via Shopify Payments), Shopify doesn''t charge extra. If you use PayPal directly on Shopify Basic, you pay an extra 2% Shopify fee on top of PayPal''s fees.'
  - q: 'Who has better chargeback protection?'
    a: 'Stripe offers free chargeback handling and $0.40 network cost on won disputes. PayPal Seller Protection covers unauthorized payments but not buyer remorse, and the fee structure is less transparent.'
  - q: 'Which has better international support?'
    a: 'Stripe supports 195+ countries and 135+ currencies with one integration. PayPal works in 200+ countries but conversion fees and holds on international accounts are stricter.'
---

PayPal and Stripe look similar on paper. The real cost difference shows up on international sales and currency conversion.

## Standard US card fees (2026)

| Feature | PayPal Checkout | Stripe |
|---|---|---|
| Online transaction | 3.49% + $0.49 | 2.9% + $0.30 |
| In-person (card present) | 2.29% + $0.09 | 2.7% + $0.05 |
| Monthly fee | $0 | $0 |
| Setup fee | $0 | $0 |
| Chargeback fee | $20 | $15 |

PayPal's standard online rate is **3.49% + $0.49** (often quoted as "2.99% + $0.49" — that's the older rate). Stripe is **2.9% + $0.30** for the first $1M/year processed.

The difference on a $50 sale:
- PayPal: $2.24
- Stripe: $1.75

You keep $0.49 more per sale with Stripe.

## The micro-fee trap

Both processors charge a fixed fee per transaction. For small-ticket items, this is a huge percentage:

| Sale price | Stripe cost | As % of sale |
|---|---|---|
| $5 | $0.45 | 8.9% |
| $10 | $0.59 | 5.9% |
| $25 | $1.03 | 4.1% |
| $50 | $1.75 | 3.5% |
| $100 | $3.20 | 3.2% |

Below $10, processor fees are over 6% of revenue. If you sell small items, either bundle them or switch to a flat-rate processor like Square (2.6% + $0.10 in-person, 2.9% + $0.30 online).

## International card fees

| | PayPal | Stripe |
|---|---|---|
| International card surcharge | 1.50% | 1.0% (above standard rate) |
| Currency conversion fee | 3–4% (retail rate) | 1% (wholesale rate) |
| Supported currencies | 25 | 135+ |
| Payout currencies | 56 | 50+ |

For a $100 sale to a UK customer paid in GBP:
- PayPal: 3.49% + $0.49 + 1.5% + 3.5% FX = **$8.49 total**
- Stripe: 2.9% + $0.30 + 1% + 1% FX = **$5.70 total**

Stripe saves you **$2.79 per sale** on this transaction.

## Chargeback handling

| | PayPal | Stripe |
|---|---|---|
| Chargeback fee | $20 | $15 |
| Network cost (won disputes) | — | $0.40 (US) / $15 (other) |
| Response window | 10 days | 7–14 days |
| Evidence upload | Manual form | Dashboard + API |
| Win rate (typical) | ~40% | ~40% |

Stripe's dashboard and API make evidence gathering easier. The $0.40 network fee on won disputes only applies to Visa and Mastercard (not Amex). The $15 Stripe fee is refunded if you win — PayPal's $20 is not.

## Payout timing

| | PayPal | Stripe |
|---|---|---|
| Standard payout | 1–3 business days | 2 business days (Standard) |
| Instant payout | $1.50 per payout | 1% of payout (min $0.50) |
| Hold period (new accounts) | Up to 21 days | 7–14 days |
| Hold trigger | High dispute rate, sudden volume spike | Same |

Both hold funds for new accounts. Stripe's hold criteria are more transparent.

## Buyer protection

| | PayPal Buyer Protection | Stripe (no buyer protection) |
|---|---|---|
| Unauthorized purchases | Covered | Not covered (use 3DS) |
| Item not received | Covered | Not covered |
| Item significantly not as described | Covered | Not covered |
| Cost to seller | Higher chargebacks | Lower dispute rate |

PayPal's buyer protection drives higher conversion but also higher chargebacks (especially for "item not as described" claims). Stripe relies on 3D Secure for fraud prevention, which shifts liability to the issuer.

## Hidden costs

### PayPal

- **Currency conversion spread**: 3–4% above mid-market rate
- **Cross-border fee**: 1.5% on top of standard rate
- **Inactivity fee**: None for business accounts
- **Refund fees**: Not refunded (you pay the original transaction fee)
- **Micropayment rate**: 4.99% + $0.09 (better for sub-$5 sales)

### Stripe

- **International card fee**: 1.0% on top of standard rate
- **Currency conversion**: 1% (close to mid-market)
- **ACH direct debit**: 0.8% capped at $5
- **SEPA direct debit**: €0.35 per transaction
- **Subscription billing**: +0.5% on recurring charges (invoicing is free)
- **Stripe Tax**: 0.5% of transaction volume

## When to use each

**Use Stripe if:**
- You process > $10k/month (better rates kick in at $80k/month)
- You sell internationally with non-USD customers
- You want developer-friendly APIs
- You have a subscription business

**Use PayPal if:**
- Your customers expect PayPal as a payment option (especially in EU and Asia)
- You sell on marketplaces that require PayPal
- You sell items under $5 (micropayment rate helps)
- You want buyer protection to drive conversion

## Practical setup

Most cross-border sellers use **both**: Stripe as the default, PayPal as a secondary option. Shopify Payments (powered by Stripe) gives you Stripe's rates; add PayPal as an additional gateway. Customers choose at checkout.

## Try the math yourself

Use the [Product Pricing Calculator](/tools/pricing-calculator/) to see how processor fees affect your target margin.