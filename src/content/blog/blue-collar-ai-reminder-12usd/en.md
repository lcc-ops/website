---
title: "A 12-USD-per-month 'remind me who to call' automation for blue-collar shop owners: 2 customers = $24/month MRR, with the obvious AI wedge to scale it to a real product"
description: "A side-project operator built a Google Sheet plus auto-email reminder for an HVAC shop owner: 3 months after install → reminder to push the filter-replacement follow-up; warranty window closing → reminder; last service 6 months ago → reminder. $12/month per customer. Today 2 paying customers, $24/month MRR. The case is not the $24; the case is the wedge: local service SMBs in plumbing, cleaning, lawn, auto-detailing run customer follow-up entirely in their heads and have no CRM. Adding AI to that template — auto-parsing past work orders, generating personalized reminders, predicting service cycles — turns a $12 retainer into a $50-$100/month product."
pubDate: 2026-07-12
category: 'ai'
tags: ['ai', 'blue-collar', 'local-services', 'reminder', 'case-study', 'monetization']
translationKey: 'blue-collar-ai-reminder-12usd'
tldr: "A Google Sheet plus auto-email reminder service for HVAC and other local trades, charging $12/month per customer. Two paying customers today, $24/month MRR. The interesting move is the AI wedge: replace manual data entry with AI-parsed past work orders, replace generic reminders with personalized messages, add predictive maintenance alerts. That turns $12/mo per customer into a $50-$100/mo product — and there is essentially zero direct competition because no VC funds 'remind plumbers to call their clients.'"
faq:
  - q: "What does the product actually do?"
    a: "Tracks each customer's service history against a follow-up schedule: filter replacement at month 3 after install, warranty window closing reminders, 6-month-since-last-service follow-ups. Sends the operator a reminder email at the right moment. Customer-facing the product is invisible — the shop owner just gets a list of who to call this week. The build is a Google Sheet for data entry plus an n8n/Make workflow plus auto-email."
  - q: "What does the case make today?"
    a: "$24/month MRR from two customers paying $12 each. The case author signals this is a side project, not the main gig. The interesting number is not $24, it is the wedge: plumbing, cleaning, lawn care, auto-detailing — these owner-operators track follow-up in their heads, not in a CRM. They have never had this kind of tool offered to them at any price."
  - q: "Why is the AI the wedge?"
    a: "Three AI features turn a $12 retainer into something a customer will pay $50-$100/month for. First, AI auto-parses past work orders: the operator drops photos of old invoices and the model extracts customer name, service date, service type. Second, personalized reminder copy: not 'your filter is due,' but 'Mr. Zhang, the Gree unit we installed is now at 3 months, can we schedule this Saturday afternoon?' Third, predictive alerts: based on cross-customer service-cycle data, the system tells the operator 'this unit tends to fail at month 18, consider proactive outreach.' Each feature individually is a 3-5x price increase on the original $12."
  - q: "Why is the competition near zero?"
    a: "Because no VC will fund 'an app that helps plumbers send follow-up texts.' The TAM per vertical is small (plumbers in one city), the buyer has never paid for SaaS before, the ACV is $12-$100/month, and the acquirer space is crowded with generic vertical SaaS that plumbers do not adopt. The result is that the operator in this case has zero direct competitors in their city. The defensibility comes from the boringness of the space, not from technology."
  - q: "What is the realistic path to scale?"
    a: "Pick one local trade first — HVAC, plumbing, cleaning, or auto-detailing — and run the playbook to 10-20 customers in one city at $50-$100/month each. That is $500-$2000/month MRR per city, per trade. Replicate across 10 cities and the same trade, where the playbook is just door-knocking Chambers-of-Commerce events and asking the question 'who do you mean to call this week?' That is a 100-customer business at $5K-$10K/month MRR, no funding, no app, no platform."
  - q: "What does the case not cover?"
    a: "Six gaps. (1) Real churn — 2 customers paying $12/month does not tell us whether a third customer, or a tenth, will stay. (2) Adoption friction — does the shop owner actually open the email and act on it? The case talks about sending reminders, not about whether the follow-up call happens. (3) Privacy / consent — using past invoice photos for AI training raises a customer-side data question the case does not touch. (4) Cash-effective margins — Google Sheets plus n8n is mostly free, but the AI features planned for v2 will incur API costs that need to be recovered in the $50-$100 price tier. (5) Geographic portability — the case is implicitly China-local; the SMB-side dynamic in the US is different. (6) Long-term exit — there is no platform exit because the product is intentionally narrow."
---
An HVAC shop owner had a recurring revenue problem that most operators solve by memory: who is due for a filter check, whose warranty is about to expire, who has not been called in 6 months. A friend built him the most boring version of a CRM — Google Sheet plus an automated email reminder — and charged $12/month for it. Two months in, a neighbor shop signed on. Two customers at $12, $24/month MRR.

That is the entire setup. The interesting part is not the $24. The interesting part is the wedge that turns boring into a real product.

## Numbers

```
Customers today:                     2
Price per customer:                  $12 / month
Total MRR:                           $24 / month
Hours per customer per month:        ~0.5 hours
Operator effective rate:             essentially passive (the 0.5h is data import + exception handling)
Tap market size per vertical:        local HVAC, plumbing, cleaning, lawn care, auto-detailing
Estimated AI-tier price:             $50 - $100 / month per customer
Estimated AI-tier margin:            similar to $12 tier (mostly n8n + AI API)
Path to $5K-$10K/month MRR:         100 customers across 1 trade in multiple cities
Time to first paying customer:       ~1 week from "I have an idea" to "first $12 invoice"
```

The interesting row is the AI-tier price. At $50-$100/month the same operator's MRR scales 4-8x without acquiring a single new customer, just by upgrading the existing product.

## Why this works in a market where most SaaS does not

The target buyer in this case is a shop owner. The local trade shop owner — HVAC, plumbing, cleaning, lawn care, auto-detailing — runs customer follow-up entirely in their head. Not in a CRM, not in Salesforce, not in Excel. They use "oh shit I forgot to call that customer." Any SaaS that costs $300/month and takes three hours to set up will not be adopted by this segment; that is the reason most vertical SaaS in blue-collar verticals dies. The product in this case is $12/month and the only onboarding is filling out a Google Sheet template. That is the only reason it has 2 customers today.

The market dynamic is also unusual. Vertical SaaS targeting blue-collar trades has been funded many times and failed many times, because the TAM per vertical is small, the buyer has never paid for SaaS, and the ACV is too low for traditional SaaS economics. The result is no incumbent. The operator in this case has no direct competitor in their city, and likely has none anywhere.

## The AI wedge — three upgrades that change the unit

```
Feature 1: AI auto-parse past work orders
  Operator drops photo of old invoice into a folder
  Model extracts customer name, service date, service type
  Auto-creates the follow-up tasks
  Replaces the manual Google Sheet entry
  Price impact: $12 -> $30-$40/mo

Feature 2: Personalized reminder copy
  Generic: "Your filter is due."
  Personalized: "Mr. Zhang, the Gree unit we installed is now at 3 months.
                  Can we schedule this Saturday afternoon?"
  Model pulls historical service notes and generates copy per customer
  Price impact: $30-$40 -> $50-$70/mo

Feature 3: Predictive service cycles
  Cross-customer data: "this unit tends to fail at month 18"
  System prompts the operator before the customer even thinks to call
  "We noticed Mr. Wang's neighbor had an issue with his unit last month;
   we recommend a quick check on Mr. Wang's similar model."
  Price impact: $50-$70 -> $80-$120/mo

Stacked, the AI wedge turns $12 into $80-$120/month per customer.
Total revenue per customer over 24 months: $1,300-$2,800
versus the boring $288 over 24 months at $12.
```

Each upgrade individually is a 2-3x price increase. Stacked, it is 8-10x. The build cost per customer is roughly the same — one Google Sheet template plus one n8n workflow plus a prompt — so the margin scales similarly.

## What this case does not cover

Six gaps. First, real churn — two customers does not tell us whether a fifth or a tenth customer will stay. Second, adoption friction — the case talks about sending the operator a reminder email, but does not confirm whether the operator actually opens the email and follows up. Third, data-consent — feeding past invoice photos to an AI for parsing raises a customer-side data question the case does not address. Fourth, cash-effective margins — Google Sheets plus n8n is essentially free at $12/month, but the AI-tier features at $80-$120/month will need API cost recovery that the case does not break out. Fifth, geography — this is implicitly the China-local SMB dynamic; the US SMB dynamic has different procurement patterns and different costs to acquire. Sixth, long-term exit — there is no platform exit because the product is intentionally narrow.

## Take-away

The wedge is that the most boring SaaS line item in a contractor's budget — "the reminder system" — has no incumbent because VCs will not fund it. AI turns that boring into something with real margin, and the local trade segment is large enough in aggregate to support a 100-customer business at $5K-$10K/month MRR without raising a dollar.
