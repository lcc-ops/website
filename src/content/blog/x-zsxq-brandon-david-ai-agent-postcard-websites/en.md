---
title: '$420 in postcards, an AI agent named David, and 8,000 USD/month MRR: a read of Brandon Doyle''s local-business website playbook'
description: 'A Utah-based operator spent $420 on a postcard mailer to 350 small local businesses, with each postcard linking to a website an AI agent had already built for the recipient. The first-month conversion produced $8,000 in MRR. A read of the unit economics, the offline-to-online conversion funnel, and the failure modes the post leaves out.'
pubDate: 2026-07-23
category: 'pricing'
tags: ['local-services', 'ai-agent', 'cold-outreach', 'postcard', 'mrr', 'case-study']
translationKey: 'x-zsxq-brandon-david-ai-agent-postcard-websites'
tldr: 'A Utah operator spent $420 printing and mailing postcards to 350 local small businesses. Each postcard linked to a website an AI agent had already built for the recipient. First-month conversion produced 8,000 USD in MRR from $420 in offline ad spend. The implied economics: every $1 of postcard spend generated ~$19 of MRR in month one. The post is silent on the month-2 retention rate, the per-customer support load, and the geographic radius that decides whether the playbook scales past one operator.'
faq:
  - q: "What is Brandon Doyle's local-business website playbook?"
    a: 'He used an AI agent (named David, his own product at getdavid.ai) reachable via iMessage to scan Google Maps for local small businesses in Utah that had a physical storefront and reviews but no website or a clearly outdated one. The agent generated a custom landing page for each business, then designed a postcard with the business name, a one-line teaser, and a QR code linking to the live page. Brandon printed 350 postcards for $420 and mailed them. Merchants who replied and asked to keep the site converted to monthly managed-hosting customers at $50–300/month.'
  - q: "What is the unit economics per merchant?"
    a: 'AI generation cost is fractions of a cent per landing page (the post says 350 sites total cost less than $20 in AI tokens). Postcard print + mail is $1.20 per piece. Total cost-to-deliver per merchant is ~$1.25. At a $100/month managed-hosting price, the customer pays back the acquisition cost in the first 4 days. At $50/month, the customer pays back in the first 8 days. Standard SMB churn is 3–7%/month, so a 1,000-customer book produces 30–70 monthly cancellations that must be backfilled.'
  - q: "What is the conversion rate?"
    a: 'The post implies roughly 30–80 merchants (10–25% of the 350 mailers) replied asking to keep the site. Of those, an undisclosed fraction converted to paying monthly customers at $50–300/month. The math implies 50–150 paying customers to clear 8,000 USD/month at the median $100 price point. The reply rate and the reply-to-customer conversion rate are the load-bearing variables.'
  - q: "Why does the offline mailer work better than online cold outreach?"
    a: 'Three reasons. (1) Open rate: physical mail has a 90%+ open rate vs 2% cold-email open rate. (2) The QR code links to a finished product, not a sales pitch — the merchant sees their name on a real site. (3) The merchant feels no urgency to act, so the perceived risk is low. Cold email triggers spam filters; the postcard skips the entire inbox.'
  - q: "What is the failure mode?"
    a: 'Three. (1) Geographic radius — once a city is saturated, the playbook needs to move to a new city. The post is silent on whether the playbook repeats in adjacent metros. (2) Quality drift — an AI-generated site that gets a merchant''s hours wrong or maps the wrong address triggers a complaint. The post does not name the QA loop. (3) Customer support load — 100+ SMB customers on managed hosting generate 5–15 support tickets per week, each 15–45 minutes. The post does not name this cost.'
  - q: "What does the post leave out?"
    a: 'Four gaps. (1) The geographic radius that decides whether the playbook scales past one operator. (2) The reply-to-customer conversion rate, which is the load-bearing variable. (3) The QA loop on AI-generated sites — a wrong address or wrong hours produces a public complaint. (4) The per-customer support cost that scales linearly with the book. The post is silent on all four.'
---

A Utah-based operator (Brandon Doyle, founder of getdavid.ai) spent $420 printing and mailing postcards to 350 small local businesses. Each postcard linked to a website an AI agent had already built for the recipient. The first-month conversion produced $8,000 in monthly recurring revenue (MRR) plus an extra $300/month from a side project. The implied economics: every $1 of postcard spend generated roughly $19 of MRR in month one. What follows is a read of the unit economics, the offline-to-online conversion funnel, and the failure modes the post does not name.

## The flow

| Stage | What happens | Cost / output |
|---|---|---|
| Scan | Agent queries Google Maps for SMBs with storefront + reviews but no/poor website | $0 in API |
| Build | Agent generates a custom landing page per business | <$20 total for 350 sites |
| Print | 350 postcards with business name, tagline, QR code | $420 |
| Mail | USPS delivery | included in print |
| Convert | Recipients scan QR, see finished site, ask to keep it | Reply rate 10–25% (implied) |
| Bill | Convert replies to managed-hosting customers | $50–300/month per customer |

The entire flow is reachable through iMessage — the operator's role collapses to (a) telling the agent which city to scan, (b) approving the postcard design, (c) handling replies from interested merchants.

## Per-merchant unit economics

| Line item | Cost | Notes |
|---|---|---|
| AI generation per site | $0.05–0.20 | Single-page, minimal assets |
| Postcard print + mail | $1.20 | Standard 4x6 USPS EDDM |
| **Total cost-to-deliver per merchant** | **~$1.25** | Before operator time |
| Operator time per merchant | 5–15 min | Reply handling, customization |
| **Payback at $100/month** | **38 hours** | First 4 days of revenue |
| **Payback at $50/month** | **76 hours** | First 8 days of revenue |

A $100/month customer pays back the acquisition cost in the first 4 days. A $50/month customer pays back in 8 days. Both are well within standard SMB churn windows (3–7%/month), so the LTV math works without any clever retention layer.

## Why offline mail beats online cold outreach

Three reasons, each with a number:

1. **Open rate.** Physical mail: 90%+. Cold email: 2%. The postcard is opened. The email is filtered or ignored.
2. **Pre-built proof.** The QR code lands on a real, finished site with the merchant's name on it. Cold email points to a sales pitch. The merchant sees their business represented, which is the persuasion event.
3. **No urgency, low perceived risk.** A merchant can scan, browse, and decide over a week. There is no "schedule a call" pressure, no calendar invite, no Zoom. The decision happens at the merchant's pace, which means the no-decision rate is lower.

The cost ratio is roughly 60x in favor of the postcard at the open-rate step, and the conversion step is multiplied by the same 60x on top of that. The post is correct that cold email is dead for SMB outreach at this scale; the postcard is the channel that survives.

## The conversion funnel the post skips

The post implies 350 mailers → first-month $8,000 MRR. The numbers behind it:

| Step | Implied rate | Output |
|---|---|---|
| Mailed | 100% | 350 |
| Scanned QR | 10–25% (typical SMB direct-mail response) | 35–90 |
| Asked to keep the site | 50–80% of scanners | 18–70 |
| Converted to paying | 30–60% of askers | 5–40 |
| **Paying customers in month 1** | | **5–40** |
| **At median $100/month** | | **$500–4,000 MRR** |

To hit $8,000 MRR in month 1, the operator needs either a higher median ticket ($200–300/month) or a larger reply population (1,000+ mailers). The post implies the higher-ticket path; the post does not name the median ticket or the mailer count that produced the $8,000.

## Three failure modes

1. **Geographic radius.** Once a city is saturated, the playbook needs to move to a new city. The post is silent on whether the playbook repeats in adjacent metros at the same economics. Reasonable expectation: it does for the first 3–5 cities, then response rates decay as the channel becomes saturated.
2. **Quality drift.** An AI-generated site that gets a merchant's hours wrong or maps the wrong address triggers a complaint that becomes a public 1-star review. The mitigation is a 5-minute human QA loop on every generated site before the postcard goes out. At 350 sites per city, the QA loop is 30 hours per city, which the post does not name.
3. **Support load.** 100+ SMB customers on managed hosting generate 5–15 support tickets per week, each 15–45 minutes. At 10 tickets/week × 30 minutes, that is 5 hours/week of operator time, scaling linearly with the customer book. The post does not name this cost.

## Bottom line

The $420-to-$8,000-MRR playbook works at the unit level. The math behind it — $1.25 per merchant delivered, $50–300/month per customer, 10–25% QR reply rate — is what makes the first-month economics real. The durability question is geographic (does the playbook scale past the first few cities?) and operational (does the support load grow linearly with the book?). The case sells the first month. The business is the second-year retention curve.