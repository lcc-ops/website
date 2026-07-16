---
title: 'The 17M USD a year an AI photo app kept by switching its payment rail off the App Store'
description: 'A small AI photo-and-video team reportedly grew 2025 revenue 14x to 55M USD annualized, then to 70M USD. Same users, same product, different checkout. The 30% Apple cut is the lever most operators forget to pull.'
pubDate: 2026-07-06
category: 'ai'
tags: [payment-fees, ai, consumer-app, monetization, payment-rail, case-study]
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
