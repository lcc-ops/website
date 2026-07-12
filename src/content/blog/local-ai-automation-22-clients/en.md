---
title: 'A US freelancer left $40/hr WordPress work, built an n8n + Claude lead-routing pipeline for local service businesses, and now runs 22 clients at $21K/month recurring'
description: "A freelance operator in the US used n8n plus Claude to build a single lead-qualification template for plumbers, dentists, HVAC, real-estate — same flow, different industry each time. 22 clients paying $300/month retainer plus $3,500 one-time setup. The math: 22 × $300 = $6,600/month locked, plus 3-4 new signups per month at $10K-$14K, totals a stable $21K+ per month. Weekly billable hours < 15. The interesting point is not the money, it's that the operator sells one template, not a software product."
pubDate: 2026-07-12
category: 'ai'
tags: ['ai', 'local-ai', 'freelance', 'side-hustle', 'case-study', 'monetization']
translationKey: 'local-ai-automation-22-clients'
tldr: "A US freelancer moved off $40/hr WordPress, built one lead-qualification workflow on n8n + Claude, and now bills 22 local service businesses at $3,500 setup plus $300/month retainer. Revenue: $21K/month recurring with fewer than 15 billable hours per week. The unit is the template, not the software: same plumbing logic applied to dentists, HVAC, real-estate, lawyers — each new client is a copy with industry vocabulary swapped. The interesting data point: setup at $875/hr effective rate vs the $40/hr ceiling he came from."
faq:
  - q: "What does the actual product look like?"
    a: "One n8n workflow that hooks into a customer's website contact form. Submission lands → Claude reads the message, scores intent from budget, timeline, location → high-intent leads push to a calendar booking link, low-intent leads receive a useful follow-up email. Setup takes 4 hours per customer. Monthly retainer covers monitoring, prompt tweaks, and silent API breakage fixes."
  - q: "How does the pricing work?"
    a: "$3,500 one-time setup fee per client, plus $300/month retainer. With 22 clients on retainer the locked-in monthly revenue is 22 × $300 = $6,600. The variable side is 3-4 new client signups per month at $3,500 each, which adds $10K-$14K. Total monthly revenue sits at $21K+, with weekly billable hours under 15."
  - q: "Why is this a freelance business and not a SaaS?"
    a: "Three structural reasons. First, the buyer is the owner of a small local business who has zero time to learn n8n or even ChatGPT. They will never self-serve. Second, the workflow is bespoke per customer (different CRMs, different calendars, different lead sources) — the per-customer setup prevents a self-serve product. Third, the operator delivers in 4 hours because Claude writes the n8n JSON config from natural-language specs, so the marginal customer is profitable only at freelancer margin, not at SaaS margin."
  - q: "Where does the customer acquisition come from?"
    a: "Local chambers of commerce events, Yelp search filtered to businesses with 50+ reviews and a 3.5-4.0 star rating (the signal for lead leakage), Facebook local business groups. No portfolio site, no SEO, no content marketing. The first five clients came purely from one referral network. Upwork exists but is not used — competitors there bill $50/hr and do not prospect local brick-and-mortar."
  - q: "What does the AI actually do in this business?"
    a: "Claude is doing the implementation work, not the customer-facing work. The operator describes the workflow in natural language and Claude outputs the n8n JSON node configuration. Without Claude the same implementation would take 20+ hours of manual JSON authoring. With Claude the time drops to 4 hours. The customer-facing AI (the lead scoring) uses Claude too, but that part is a thin wrapper — the economic leverage is in the build-time compression."
  - q: "What does the case not cover?"
    a: "Five gaps. (1) Churn rate — the operator does not publish monthly client cancellation rate; 22 clients at any moment does not tell us how many leave per year. (2) Setup payment terms — $3,500 paid upfront or split? Affects cash flow. (3) Gross margin per project — Claude API costs, n8n hosting, and the 1-2 support hours per client per month are not separated out from the hourly rate. (4) Geography — this is a US-local case, and China-side SMBs have different willingness-to-pay plus WeChat-as-CRM dynamics. (5) Defensibility — 22 clients today, but there is no lock-in past the next month if a cheaper operator appears."
---
A US-based freelancer used to cap at $40/hour on WordPress builds. Around the end of 2025 he shifted to a different offer: an AI lead-qualification workflow on n8n plus Claude, sold to local service businesses with no in-house technical staff. By June 2026 the operator is running 22 such customers and billing above $21K every month, working fewer than 15 hours per week.

The interesting lever is not the AI model, it is the reuse of one template across industries. The workflow is "website form submit → Claude scores intent → high-intent routes to a calendar booking link, low-intent gets a useful follow-up email." That same flow, swapped into a dental clinic, an HVAC shop, a real-estate team, a lawyer, a cleaning company, is a new paying customer. The number of features shipped is one.

## Numbers

```
One-time setup fee per customer:      $3,500    (installs the n8n + Claude pipeline)
Monthly retainer per customer:        $300      (monitoring, prompt tuning, API drift fixes)
Locked-in monthly revenue:           $6,600    (22 retainers × $300)
New client signups per month:        3 to 4    (at $3,500 each = $10.5K-$14K)
Total monthly revenue:                $21K+     (retainer base + new signups)
Setup time per customer:             4 hours   (with Claude writing the n8n JSON)
Weekly billable hours:                < 15
Effective setup rate:                ~$875/hr  ($3,500 / 4h)
```

The numbers in the row for "weekly billable hours" come from the case author's own framing — fewer than 15 hours per week on customer work. Above-the-fold revenue math, not bill-rate math.

## Why n8n + Claude at this position

The choice of n8n plus Claude is not interchangeable with "any workflow tool plus any LLM." n8n gives the operator a visual node-graph plus JSON export, which Claude can write and the operator can debug. Make.com and Zapier work the same way; Zapier is more polished for non-technical users, n8n is cheaper at scale and has a self-host option. The model layer (Claude) is replaceable; the workflow tool is replaceable; the structure is not — one template, many industries.

Three reasons this template hits. First, the target buyer is a small business owner who has heard of ChatGPT but does not know how to wire it into a workflow. They will never self-serve, and they will not read a 30-page RFI. Second, the lead-qualification outcome is concrete and cheap to demonstrate — "your site form leads will get a personalized reply in 90 seconds, day and night." Third, the operator's customer-acquisition channel is local — chambers of commerce events, Yelp signals, Facebook local business groups — which Upwork freelancers at $50/hr do not prospect.

## The unit economics in detail

```
Setup cost (4 hours at operator's effective rate):         $3,500 revenue, $0 explicit
Claude API cost during setup:                              ~$5-15 per customer
n8n hosting cost during setup:                             ~$0 (self-hosted or free tier)
Monthly retainer revenue:                                  $300 / month
Monthly support hours per client:                          1-2 hours average
Gross margin per client per month:                         ~$240-280 / month
Month-1 cash flow on a new client:                         $3,500 setup + first $300 retainer
Month-2 onward cash flow per existing client:              $300 / month pure retainer
22 clients × $300 / month retainer:                        $6,600 / month locked-in
```

A subtle data point: the operator does not charge for support hours above the retainer. Customer escalations are absorbed into the per-month $300. If monthly support hours exceed 1-2 per customer, the margin compresses. The case author treats this as a known constraint — "the simple workflow, the harder the job" is the rule he keeps repeating.

## What this case does not cover

Five gaps. First, churn — the operator does not publish customer retention rate; 22 customers at any point in time does not tell us how many leave per year. Second, setup payment terms — is the $3,500 paid upfront, 50/50, or financed against the first month retainer? That affects cash flow and bad-debt risk in a way this case does not touch. Third, gross margin per project — Claude API spend, n8n hosting, and the unflagged support hours are not broken out. Fourth, geography — this is the US small-business market, which has different willingness-to-pay and different CRMs than the China SMB market that an operator reading in Shanghai would face. Fifth, defensibility — 22 customers today, but nothing prevents a $50/hr competitor from prospecting the same local channels next year and undercutting the $3,500 setup fee.

## Take-away

The structural lesson is that one workflow sold 22 times with industry vocabulary swapped is more profit than any software product the same person could have built. The compounding is in the customer count, not the feature count.
