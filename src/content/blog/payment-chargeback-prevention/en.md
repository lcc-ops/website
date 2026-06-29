---
title: 'How to Prevent Payment Chargebacks (and Win Disputes When They Happen)'
description: 'Practical chargeback prevention for cross-border ecommerce. Covers fraud screening, 3DS, evidence templates, and the dispute process on Stripe and PayPal.'
pubDate: 2026-06-29
category: 'payment'
tags: ['chargeback', 'fraud', 'dispute', 'prevention']
translationKey: 'payment-chargeback-prevention'
tldr: 'Enable 3D Secure on all transactions, ship to the card billing address only, respond to disputes within 7 days with tracking + communication logs, and avoid signature-required delivery (it increases disputes).'
faq:
  - q: 'What is a chargeback fee in 2026?'
    a: 'Stripe: $15 per dispute, refunded if you win. PayPal: $20 per dispute, not refunded. Visa and Mastercard also charge a $0.40–$0.95 network fee on won disputes.'
  - q: 'How long do I have to respond to a chargeback?'
    a: 'Stripe gives 7–14 days depending on the card network. PayPal gives 10 days. Missing the window means automatic loss — calendar reminders are critical.'
  - q: 'Does 3D Secure prevent chargebacks?'
    a: 'Yes — for "unauthorized purchase" disputes (cardholder fraud), 3DS shifts liability to the issuer. It does not prevent "item not received" or "not as described" disputes, which require evidence.'
  - q: 'What is the chargeback win rate for ecommerce?'
    a: 'Average 40% across all categories. Sellers with detailed tracking + customer communication logs win 60–80%. Sellers who ignore disputes win under 10%.'
  - q: 'Should I block customers who file chargebacks?'
    a: 'Yes, on the card number and email. Stripe Radar and PayPal Seller Protection both let you blacklist. Repeat offenders cost more than they spend.'
---

A chargeback isn't a refund. It's a $15–20 fee plus the product cost plus your time — even if you win. Prevention is cheaper than defense.

## The two types of chargebacks

### 1. Unauthorized (cardholder fraud)

Someone used a stolen card to buy from you. The real cardholder notices and disputes. With 3DS in place, liability shifts to the issuer. Without 3DS, you eat the loss.

**Win rate with 3DS**: ~85% (issuer pays)
**Win rate without 3DS**: ~40% (you eat it)

### 2. Merchant disputes (buyer remorse)

- **Item not received** (INR) — buyer claims product didn't arrive
- **Significantly not as described** (SNAD) — product differs from listing
- **Service not provided** — digital products, services

These need evidence, not fraud filters. **Win rate with strong evidence: 60–80%**.

## Prevention checklist

### Before the sale

- [ ] **Enable 3D Secure** on all transactions. Stripe and PayPal both support it. Conversion drops 3–5%, but chargebacks drop 50%+.
- [ ] **Use AVS** (Address Verification System). Mismatched billing/shipping is a fraud flag.
- [ ] **CVV required** — never waive it. Most fraud doesn't have the CVV.
- [ ] **Velocity checks** — flag 3+ orders from same IP/card in 24h.
- [ ] **Block high-risk countries** if you don't ship there. List available in Stripe Radar.
- [ ] **Require signed delivery** — actually, don't. Signed delivery increases disputes because buyers must be present, often during work hours.

### At checkout

- [ ] **Clear billing descriptor** — use a recognizable name. "STORE NAME 12345" not "TXN*987XYZ".
- [ ] **Order confirmation email** — sent immediately, includes order number, items, total, expected delivery.
- [ ] **Shipping confirmation email** — sent when label created, with tracking number.
- [ ] **Real-time tracking** — send delivery updates as the package moves.

### After the sale

- [ ] **Proactive communication** — if shipping is delayed, email the buyer BEFORE they contact you. Reduces INR disputes by 40%.
- [ ] **Easy refund path** — make "request a refund" obvious. Buyers who can easily refund rarely chargeback.
- [ ] **Respond to all messages within 24h** — silence drives chargebacks.
- [ ] **Generous return policy** — 30 days, free returns. The cost is less than chargeback fees.

## What to include in a dispute response

### For "item not received"

1. Tracking number with carrier name
2. Carrier-delivered status with delivery date and location
3. Signature (if you have it)
4. Customer's IP address at order placement
5. Customer's email correspondence (any "where is my order?" replies you sent)

### For "not as described"

1. Original product listing (screenshot + URL)
2. Photos of the actual product shipped
3. Supplier/manufacturer description
4. Customer's signed delivery confirmation
5. Any prior communication about the product

### For "unauthorized purchase"

1. 3DS authentication record (CAVV / ECI value)
2. AVS match (billing = shipping address)
3. CVV match
4. Customer's order history (reputable or first-time)
5. Device fingerprint and IP geolocation matching billing address

## Stripe dispute response template

```
Subject: Dispute evidence for order #12345

We dispute this chargeback. The cardholder authorized this purchase.

ORDER DETAILS
- Order ID: 12345
- Date: 2026-06-15
- Amount: $79.99
- Items: 1x Premium Widget

PROOF OF DELIVERY
- Carrier: USPS
- Tracking: 9400111899223456789012
- Status: Delivered 2026-06-18 at 14:32 to 123 Main St, Anytown, CA
- Signed by: J. SMITH

PROOF OF AUTHORIZATION
- AVS: Full match (billing = shipping)
- CVV: Match
- 3DS: Authenticated (ECI 05, CAVV provided)
- IP: 73.118.42.xx geolocated to Anytown, CA
- Email: customer@gmail.com (matches billing name)

CUSTOMER COMMUNICATION
- 2026-06-15: Order confirmation sent
- 2026-06-18: Delivery confirmation sent
- No customer contact received disputing the order
```

## PayPal dispute response template

```
We dispute this claim. Order was delivered to the address provided by the buyer.

Tracking number: 1Z999AA10123456784
Carrier: UPS
Status: Delivered [date] at [time] to [address]

The buyer's PayPal-registered address matches the shipping address.
The buyer has not contacted us to report any issue.

Attached:
- Carrier delivery confirmation (PDF)
- Original order invoice
- Customer signature on delivery
- Email correspondence showing no prior complaint
```

## What NOT to do

- **Don't refund the customer and accept the chargeback** — you'll be charged twice (refund + chargeback fee).
- **Don't ship to a different address than the billing address** — almost guaranteed loss.
- **Don't use generic dispute text** — each dispute needs specific evidence.
- **Don't ignore deadlines** — calendar reminder the moment a dispute opens.
- **Don't argue with the customer** — communicate professionally; legal threats backfire.

## When prevention isn't enough

Some chargebacks are inevitable. Track the rate:

- **< 0.5%** of transactions: healthy
- **0.5–1%**: borderline; review processes
- **1–1.5%**: high; you'll be flagged by the network
- **> 1.5%**: in a monitoring program; expect account holds

If your rate climbs, audit:

1. New product listings (is something misleading buyers?)
2. Shipping carriers (delivery delays driving INR disputes?)
3. Recent customer service complaints (unresolved issues becoming disputes?)

## Tool: dispute tracking

Build a simple spreadsheet:

| Order ID | Dispute opened | Reason | Amount | Fee | Evidence sent | Status | Resolved date |
|---|---|---|---|---|---|---|---|
| 12345 | 2026-06-20 | INR | $79.99 | $15 | Tracking + email | Won | 2026-06-28 |

Review monthly. Patterns reveal which products, which shipping methods, which customer segments cause the most disputes.

## Try the math

Use our [Product Pricing Calculator](/tools/pricing-calculator/) to model chargeback costs into your pricing.