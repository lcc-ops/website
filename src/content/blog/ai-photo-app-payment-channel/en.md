---
title: 'The 17M USD a year an AI photo app kept by switching its payment rail off the App Store'
description: 'A small AI photo-and-video team reportedly grew 2025 revenue 14x to 55M USD annualized, then to 70M USD. Same users, same product, different checkout. The 30% Apple cut is the lever most operators forget to pull.'
pubDate: 2026-07-06
category: 'ai'
tags: ['ai', 'consumer-app', 'monetization', 'payment-rail', 'case-study']
translationKey: 'ai-photo-app-payment-channel'
tldr: 'A consumer AI photo-and-video team reportedly took revenue from 55M USD annualized to 70M USD annualized by routing most of the funnel through a self-hosted web checkout instead of the App Store. Same users, same product, different payment rail. The implied delta is 17M USD/year for swapping one payment rail — larger than most teams spend on model fine-tuning in a quarter.'
faq:
  - q: "What is the actual revenue gap?"
    a: 'The case puts two numbers on the table: 55M USD annualized (earlier 2025 number) and 70M USD annualized (early 2026 number). The implied delta is 15M USD, and the company says most of that comes from rerouting subscriptions to its own web checkout. The full-year effect, applied to the larger 70M base, is 17M USD of gross that would otherwise have gone to Apple.'
  - q: "How does the App Store cut work against a consumer AI app?"
    a: 'Apple takes 30% (15% for the small-business program if revenue stays under 1M USD/year per app, which is irrelevant at this scale). On 70M USD of subscription revenue, that is 21M USD of platform fee. A web checkout with Stripe or Paddle charges roughly 2.9% + 0.30 USD per transaction. The break-even on building and maintaining the web funnel is recovered inside one quarter at this revenue level.'
  - q: "What is the funnel structure?"
    a: 'The case describes a two-step funnel: ads land users on a self-hosted pricing page first, the user pays on the web, and only then is invited to download the native app for ongoing use. The app is for retention and daily engagement; the web checkout is for new acquisition. This splits the user journey so the acquisition cost can be measured against the actual paid conversion, not against app installs.'
  - q: "Does the company actually train its own model?"
    a: 'No. The case explicitly says the team does not train a base model and instead wraps third-party image and video models (commercial APIs and a few open-source ones) behind ~1,000 preset "styles". Each preset is a one-click workflow that turns a user prompt into a finished image or short video. The user does not see model parameters; they see outcomes.'
  - q: "What is the growth engine behind the 14x?"
    a: 'The case attributes the growth to the combination of (a) ~1,000 preset styles, each one a piece of organic-shareable social content, (b) ~1 billion cumulative renders across the catalog, which feed back into the style discovery loop, and (c) the web funnel, which converts ad spend at a measurable CAC and feeds cohort data back to the ad platform. The company says it scaled Apple Search Ads budget 13x in one year on the back of that data.'
  - q: "What does the case leave out?"
    a: 'Four things: (1) gross margin after the model-API bill — third-party model cost is non-trivial and the case does not name a unit-economics table; (2) what happens to retention if Apple changes rules again on out-of-app checkout links; (3) the cost of building and maintaining a payment, tax, and refund pipeline in 30+ jurisdictions; (4) regulatory exposure of processing subscription payments outside the App Store, which Apple has actively litigated against. The case is silent on all four.'
---
A small team running a consumer AI photo-and-video app reportedly grew revenue 14x in 2025, hit 55M USD annualized, and is now at 70M USD annualized. The product did not get a major model upgrade in that window. The growth came mostly from one operational decision: most of the paid funnel now runs through a self-hosted web checkout instead of the App Store. Below is what the case puts on the table and what it does not.

## The numbers

| Quantity | Value |
|---|---|
| 2025 revenue growth | 14x year-over-year |
| Annualized revenue (2025) | 55M USD |
| Annualized revenue (early 2026) | 70M USD |
| App Store category rank | Top 5 in Photo & Video |
| Funding | None (bootstrapped) |
| Styles (preset templates) | ~1,000 |
| Cumulative renders | ~1 billion |

The figures are company-attributed. Not audited. They are useful as a directional argument, not as a financial statement.

## The payment-rail math

The case lays out the cut in concrete numbers:

```
70M USD routed through App Store  →  49M USD net (after 30%)
70M USD routed through own web checkout  →  ~66.5M USD net (after ~5% blended)
                                                          Δ ≈ 17.5M USD/year
```

That is the headline number. The case is explicit: same users, same product, different checkout. The 17M USD is more than most AI consumer teams spend on model API costs in a quarter.

A second, quieter lever sits next to the cut: tax and refund handling. On the App Store, Apple handles VAT collection, sales-tax remittance, refunds, and chargebacks. On the web checkout, that work moves to the operator. At 70M USD of GMV, that is a real payroll line. The case does not name the cost, but the implication is that the team has hired for it.

## Why the App Store is a tax most operators forget

Most consumer AI teams go to market on iOS first because the App Store is the cheapest distribution channel with the worst unit economics. Free downloads are frictionless, but every paid conversion loses 30% to Apple, and the operator cannot see who paid, when, or how the cohort behaves. The platform owns the customer relationship.

The case describes a different pattern: iOS for retention and daily engagement, the web for new acquisition and paid conversion. Ads drive traffic to a self-hosted pricing page. The user pays on the web, gets access to the product, and is later invited to download the app for a richer experience. The app becomes the daily-driver surface; the web becomes the checkout.

This split has two structural advantages:

1. **The operator owns the paid customer.** Email, billing, churn reason, refund reason, expansion signal — all visible to the operator. Apple does not allow this data to be exported at the cohort level, and what is exported is delayed.
2. **Ad CAC becomes measurable.** If an ad keyword produces 50 paying web customers at a 30 USD CPA, the operator can scale that keyword. If an ad keyword produces 200 app installs at a 6 USD CPA but zero of them subscribe, the operator should kill that keyword. This data is what the case says drove the 13x budget scale-up on Apple Search Ads.

## The "no model" stance

The second non-obvious choice in the case is that the team does not train a base model. The product wraps ~1,000 preset "styles" over third-party image and video model APIs (commercial and open-source). Each preset is a one-click workflow — the user describes what they want, the system picks the model, applies the preset, and returns a finished output.

This is a deliberate trade. The operator does not pay the capex of training a foundation model, does not take on the inference-cost tail, and does not have to keep up with a frontier that moves every two months. In return, the operator has no model moat. The moat they are building is the catalog of 1,000 workflows, the data from 1 billion renders, and the conversion loop on the web checkout.

The case is explicit: users do not see model parameters. They see outcomes. The mental model the company sells is "three minutes from prompt to finished clip", not "which diffusion model is best for this".

## What this case does not cover

The case is detailed on what the team did. It is silent on the four points that decide whether the math replicates for another operator:

1. **Gross margin after model-API cost.** Wrapping third-party models is cheaper than training, but the API bill scales with renders. The case does not give a unit-economics table. At 1 billion renders, the model-API line is non-trivial and almost certainly the largest variable cost.
2. **Apple's policy on out-of-app links.** Apple has litigated against apps that route users to external checkout. The case does not name how the team handles the policy risk, and a policy change could force a re-architecture of the funnel overnight.
3. **Refund and chargeback overhead.** Web checkout means the team owns the dispute pipeline. At 70M USD GMV, chargebacks at industry-average 0.5–1% would be 350k–700k USD/year of operational work and potential losses.
4. **Sales-tax and VAT compliance.** The web checkout must collect and remit tax in every jurisdiction the user pays from. At global scale this is a real compliance line item and a real engineering line item. The case does not name either.

The payment-rail lever is real and large. Whether it is portable to a smaller app depends mostly on whether the operator is willing to take on the compliance and policy risk that the App Store currently absorbs.