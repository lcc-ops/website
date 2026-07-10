---
title: "2 people, 70K tickets per month at 82% auto-resolution, 0.10 USD per ticket: My AskAI's customer-support math, and the integration moat nobody talks about"
description: "My AskAI — Mike Heap in London, 2-person team. AI customer-support agent that plugs into existing ticket systems, resolves 70K tickets per month at 82% resolution rate, costs 0.10 USD per ticket. 250+ e-commerce and SaaS customers. The product sells against a human-support headcount, not a software seat. The funnel math, the integration moat, and the four gaps the case does not cover, below."
pubDate: 2026-07-10
category: 'ai'
tags: ['ai', 'customer-support', 'integration-moat', 'per-ticket-pricing', 'case-study', 'monetization']
translationKey: 'x-my-askai-2ppl-82pct'
tldr: "My AskAI — 2-person team, 70K tickets/month at 82% resolution, 0.10 USD/ticket cost, 250+ customers. Pricing anchored against human-support headcount, not software seats. The interesting part is not 'AI answers tickets' — it is the integration moat (plugs into existing ticketing, helpdesk, past agent replies). The funnel math, the integration moat, and the four gaps the case does not cover, below."
faq:
  - q: "What does the case actually document?"
    a: "My AskAI — an AI customer-support agent that plugs into existing ticketing and helpdesk systems. 2-person team in London. Customers include 250+ e-commerce and SaaS companies. Average auto-resolution rate 75%+. One customer moved from 25% to 79% resolution, saving ~150 hours/month. Another cut response time to under 60 seconds. A third saw 82% of 70K monthly tickets handled by the AI without human touch. Per-ticket cost roughly 0.10 USD."
  - q: "What is the unit economics?"
    a: "Per ticket resolved by AI: 0.10 USD cost (LLM API + infra). Per ticket resolved by human: 3–8 USD loaded cost (UK / US support agent, fully loaded). Saving per AI-resolved ticket: 3–8 USD. At 70K tickets/month × 82% resolution = 57.4K AI-resolved tickets. Customer saves 172K–459K USD/month in support costs. My AskAI's price is typically 20–40% of that saving — so per-customer revenue is 35K–185K USD/month at scale."
  - q: "What is the integration moat?"
    a: "Three layers. (1) Ticketing-system connectors — Zendesk, Intercom, Freshdesk, Salesforce Service Cloud, custom stacks. (2) Help-center ingestion — auto-ingests customer help-center articles as knowledge base. (3) Past-reply learning — auto-learns from human agent's historical replies, no manual labeling. A new entrant with a better LLM does not displace My AskAI because the moat is in the connector library and the past-reply training loop."
  - q: "Why is the 2-person team realistic?"
    a: "Because the product is operations-light. The connectors are built once and reused across customers. The knowledge-base ingestion is automated. The past-reply learning is automated. Sales is bottom-up (customer finds the product, signs up, plugs in). The 2-person team covers engineering (connector maintenance) and customer success (high-touch onboarding for the first 30 days). At scale, more engineers and CS people are needed."
  - q: "What is the risk?"
    a: "Four risks. (1) Helpdesk-side vertical integration — Zendesk, Intercom, Salesforce all ship their own AI features; they bundle it with the seat. (2) Resolution-rate ceiling — 82% is high; pushing past 90% is hard. Customer expectations rise with success. (3) Quality disputes on the 18% — the 18% that humans still handle can include the high-stakes cases (refund disputes, legal threats); one bad AI answer going viral hits the customer. (4) Per-ticket pricing volatility — if a customer shifts from 70K tickets/month to 700K, the per-ticket cost line is what the customer looks at first."
  - q: "What does the case skip?"
    a: "Four gaps. (1) Per-customer revenue is not disclosed — the 250+ customer count is impressive, but revenue per customer varies 100x (small e-commerce vs large SaaS). (2) Onboarding cost per customer is hidden — first 30 days of high-touch onboarding is engineering time; the 2-person team can only handle so many parallel onboardings. (3) The 18% human-handled case mix is not broken out — which cases does AI fail on, and what is the customer-support cost of those? (4) Competitor comparison vs Intercom Fin, Zendesk AI, Salesforce Einstein — the case does not compare resolution rates head-to-head."
---

My AskAI — Mike Heap in London, 2-person team. AI customer-support agent plugs into existing ticketing and helpdesk systems. 70K tickets/month at 82% resolution rate. Per-ticket cost 0.10 USD. 250+ e-commerce and SaaS customers. Pricing anchored against human-support headcount, not software seats. The interesting part is not 'AI answers tickets' — it is the integration moat (connectors, help-center ingestion, past-reply learning). The funnel math, the integration moat, and the four gaps the case does not cover, below.

## The per-ticket economics

```
Per ticket:
  AI-resolved cost:           0.10 USD
  Human-resolved cost:        3–8 USD (loaded)
  Saving per AI ticket:       3–8 USD

At 70K tickets/month × 82% resolution = 57.4K AI-resolved tickets
Customer saving:              172K–459K USD/month

My AskAI price (typical):     20–40% of saving
Per-customer revenue:         35K–185K USD/month at scale

Annualized per customer:      420K–2.2M USD/year
```

The per-ticket math is the core move. The customer is buying a percentage of support-cost savings, not a software seat. A seat at 99 USD/month is 1188 USD/year; a 20% share of 200K USD/month savings is 40K USD/month, or 480K USD/year. The latter is 400x the former, and the customer is happier because the bill scales with their support volume.

## Why 2 people is realistic at 250+ customers

The 2-person team is realistic because the product is operations-light. Three components compound:

1. **Connectors are built once.** Zendesk, Intercom, Freshdesk, Salesforce Service Cloud, custom stacks. Built once, reused across all customers.
2. **Knowledge-base ingestion is automated.** Customer help-center articles feed in automatically; no manual labeling.
3. **Past-reply learning is automated.** The AI learns from human agent historical replies without manual annotation.

Sales is bottom-up. Customer finds the product, signs up, plugs in. The 2-person team covers engineering (connector maintenance) and customer success (high-touch onboarding for the first 30 days). At 250+ customers the team will need to grow — 2 people cannot run 30-day high-touch onboarding for hundreds of customers in parallel.

## Why the integration moat compounds

The moat is not the LLM. Three layers compound:

1. **Connector library.** Each new connector adds another customer segment. Building a Zendesk connector takes roughly 2 engineer-weeks. Each connector unlocks a market slice.
2. **Help-center ingestion.** The product auto-ingests the customer's help-center. The more it ingests, the better it answers. A new customer with 500 help-center articles gets a usable agent on day 1.
3. **Past-reply learning.** The AI learns from the customer's own human-reply history. Customer-specific tuning compounds with usage. A 6-month customer has a substantially better agent than a day-1 customer.

A new entrant with a better LLM does not displace My AskAI because the moat is in the connector library and the customer-specific tuning.

## What this case does not cover

- **Per-customer revenue is not disclosed.** 250+ customers is impressive but revenue per customer varies 100x. A small e-commerce site at 500 tickets/month is a different deal from a large SaaS at 50K tickets/month.
- **Onboarding cost per customer.** The first 30 days of high-touch onboarding is engineering time. The 2-person team can only handle so many parallel onboardings — a 100-customer onboarding spike overwhelms the team.
- **The 18% human-handled mix.** Which cases does the AI fail on, and what is the support cost of those? High-stakes cases (refund disputes, legal threats) that humans still handle can drive the per-ticket effective cost up sharply.
- **Competitor head-to-head.** The case does not compare resolution rates vs Intercom Fin, Zendesk AI, Salesforce Einstein. Those bundles ship with the seat and have different pricing math.

## Bottom line

The model is real: 2 people, 70K tickets/month at 82% resolution, 250+ customers. The core move is pricing as a percentage of support-cost savings, not as a software seat — it scales with the customer's support volume and aligns incentives. The moat is operational (connectors, help-center ingestion, past-reply learning), not technical. A reader replicating this should pick 1 ticketing system, build that connector first, then expand. The 2-person team is realistic at 50–100 customers; past that, customer-success hiring becomes the constraint.