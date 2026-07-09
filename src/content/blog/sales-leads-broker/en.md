---
title: "Selling sales leads at $1K+/month: AI re-did the broker business"
description: "An X post (259 likes, 101 replies, 90 reposts) describes an information-arbitrage business: AI finds customers for other people (qualified leads), zero inventory, zero delivery. The product isn't the relationship — it's the structured data. The mechanism, unit economics, risk map, and four gaps the case does not address."
pubDate: 2026-07-09
category: 'ai'
tags: ['ai', 'leads', 'b2b', 'side-hustle', 'sales', 'case-study', 'monetization']
translationKey: 'sales-leads-broker'
tldr: "AI rebuilt the traditional broker business. AI scrapes public data, filters for buying signals, structures the result into 50–200 qualified leads per pack, and sells the pack to small-B sales teams at $100–$500. Low ticket price, 80%+ margin, zero inventory, zero delivery, can compound. The interesting part is not 'broker upgraded' — it is 'the cut that used to go to the broker now goes to the seller.' The mechanism, the unit economics, and the risk map."
faq:
  - q: "What is the core mechanism of the case?"
    a: "Traditional brokers sell relationships — you have to know people to make a match. The AI version sells structured data. AI scrapes public sources (LinkedIn, company sites, industry directories, social media), detects signals that 'this account is currently looking for a service like yours' (hiring, RFPs, expansion news, tech stack changes), and packages the decision-maker contact (name, title, email, recent activity) into a 50–200 lead pack. Sold at $100–$500/pack to small-B sales teams. Buyer's cold-outreach conversion is 5–10x higher than unfiltered cold call."
  - q: "What does the AI do specifically?"
    a: "Three things. (1) Scraping — AI crawls public pages, industry directories, LinkedIn posts, auto-dedupes. (2) Filtering — AI judges whether each lead is in a 'currently looking for your service' window, drops the rest. (3) Structuring — AI fills in the four fields (name / title / email / recent activity) per lead, drops it into the buyer's CRM. The three together cut one person's lead-gen from '50 leads per week' to '200 leads per day.'"
  - q: "Why is this an information-arbitrage business?"
    a: "Because what is sold is not the data itself — LinkedIn and company sites are public. What is sold is the processed product: 'filtered + ranked + timed.' A salesperson could scrape on their own, but one salesperson's weekly hours get them 50 leads of random quality. AI does 200/day filtered by signals like 'expanded in the last 7 days,' 'hiring a sales role,' 'just switched CRM.' That processing is the scarce resource, not the data."
  - q: "What is the unit economics?"
    a: "A typical pack: 100 leads sold at $200. AI scraping + filtering + structuring costs $0.5–$2/lead, so a pack costs $50–$200 to produce. Gross margin is 0–75% (typical AI-tool level). At 80% 'contact is real' (not 'will buy') rate, 20 packs/month = $4,000 revenue, $800 cost, $3,200 gross. One person can do this."
  - q: "How is this different from cold-call tools (Apollo, Lusha)?"
    a: "Apollo and Lusha sell tool + database. You buy it, you run it yourself. AI lead packs sell the finished product. You buy it, you use it directly, no filtering logic to run. The difference is like 'selling ingredients' vs 'selling meal kits.' Meal kits have lower ticket but higher margin, and higher switching cost (users don't easily change meal-kit brands once they pick one)."
  - q: "What does the case quietly skip?"
    a: "Four gaps. (1) Compliance — GDPR / CCPA / PIPL draw lines on B2B lead scraping. EU data sold to US sales teams can be illegal. (2) Buyer conversion — the case implies 'qualified lead = sale,' but real conversion is 1–5%; most leads won't close. (3) Retention — the case doesn't say if buyers come back. One-time vs subscription changes ARPU 5–10x. (4) Signal decay — AI catches 'last 7 days of expansion' signals, but those decay in 7 days. Price must move with signal freshness."
---
An X post (259 likes, 101 replies, 90 reposts) describes an information-arbitrage business: use AI to find customers for other people. Low ticket per pack, but 80%+ margin, zero inventory, zero delivery, and it can compound.

The case is not 'broker upgraded.' It is: AI rebuilt the traditional broker business. What is sold is not the relationship — what is sold is the structured data: who is currently looking for your kind of service, who the decision-maker is, what the email is, what they've been doing lately. The mechanism, the unit economics, the risk map, and four gaps the case does not address, below.

## The mechanism, three steps

```
Public data (LinkedIn, company sites, social media, industry directories, RFP feeds)
   ↓
AI scraping (auto-crawl, auto-dedup, auto-screen against GDPR blocklists)
   ↓
AI filtering (signal check: has this company expanded in the last 7 days?
                              Is it hiring a sales role?
                              Did it switch CRM / marketing tool?
                              Just raised funding?)
   ↓
AI structuring (each lead becomes four fields: name / title / email / recent activity)
   ↓
Finished "qualified lead pack" (50–200 leads/pack)
   ↓
Sold to small-B sales teams ($100–$500/pack)
```

The buyer's cold-outreach conversion is 5–10x higher than unfiltered cold call, because the signals are pre-filtered and the decision-maker is pre-located.

## Why this is "information arbitrage"

What is sold is not the data itself — LinkedIn and company sites are public. What is sold is the processed product: 'filtered + ranked + timed.'

A salesperson could scrape on their own, but one salesperson's weekly hours get them 50 leads of random quality. AI does 200/day filtered by signals like 'expanded in the last 7 days,' 'hiring a sales role,' 'just switched CRM.' That processing is the scarce resource, not the data.

Like 'selling ingredients' vs 'selling meal kits': Apollo and Lusha sell tool + database (ingredients); AI lead packs sell the finished product (meal kits). Meal kits have lower ticket but higher margin, and higher switching cost — once a sales team picks a lead-pack vendor, they don't switch easily.

## Unit economics

```
A typical pack: 100 leads sold at $200
AI scraping + filtering + structuring: $0.5–$2/lead, so $50–$200/pack cost
Gross margin: 0–75% (typical AI-tool level)
20 packs/month: $4,000 revenue, $800 cost, $3,200 gross
```

One person can run this. Scaling to $20K/month (100 packs) requires:
- multi-channel signal sources (LinkedIn + industry directories + RFP feeds + company news)
- signal weighting model (let AI judge that 'hiring a sales role' weighs more than 'switched CRM')
- customer segmentation (leads for SaaS sales / B2B services / e-commerce ops are different packs)

## Who buys

Two customer types:

1. **Small-B sales teams.** 5–20 people, no in-house lead-gen team, can't afford HubSpot / Salesforce full automation. Buying a finished pack is the cheapest path.
2. **Freelance salespeople.** 1–3 people running their own cold outreach, need continuous lead flow. Subscription lead packs ($500/month for 300 leads) are the common format.

Big-B sales teams (100+ people) have internal SDR / lead-gen teams, don't buy external packs.

## Risk map

Four risks:

1. **Compliance.** GDPR / CCPA / PIPL draw lines on B2B lead scraping. EU data sold to US sales teams can be illegal. Some verticals (medical, legal, financial) are stricter. The buyer's legal team can block renewal.
2. **Buyer conversion.** The case implies 'qualified lead = sale.' Real conversion is 1–5%. Most leads won't close; 'qualified' just means the contact is real. Seller is paid per pack, buyer is paid per close — expectations don't match.
3. **Retention.** The case doesn't say if buyers come back. One-time vs subscription changes ARPU 5–10x. Subscription is 'stable MRR'; one-time is 'a hunt for new customers every month.'
4. **Signal decay.** AI catches 'last 7 days of expansion' signals; those decay in 7 days. Price must move with signal freshness. 'Expanded yesterday' and 'expanded last week' are different prices. Freshness management is product differentiation.

## What the case quietly skips

Four gaps.

1. **GDPR / PIPL boundaries.** The case does not mention compliance at all. EU data sold to US sales teams can be explicitly illegal in some cases.
2. **Real buyer conversion.** 100 leads per pack, 1–5% cold-outreach conversion, that's 1–5 closed deals. The case calls the leads 'qualified' but doesn't give a 'qualified' definition.
3. **Retention vs one-time.** Lead-selling ARPU depends heavily on retention. One-time is 'find new customers every month' — different business. The case is silent.
4. **Signal-decay pricing.** 'Last 7 days of expansion' signals decay in 7 days. Price must drop as signal ages. Freshness-tiered pricing is the product differentiator. The case doesn't mention it.

## Take-away

The case is not 'use AI to be a broker.' It is: AI took the cut that used to go to the broker and gave it back to the seller. Traditional brokers take 30–50% commission; AI lead packs take 5–10% ($200/pack vs $2,000/close). Both sides are better off.

For a small-B sales team: subscription lead packs at $500–$2,000/month are 10–20x cheaper than hiring an SDR ($50K/year fully loaded).
For an independent seller: one person can do 20–100 packs/month, $4K–$20K/month. Scale via signal sources + weighting model + customer segmentation.

The real moat in lead-selling is not AI capability — that's buyable. It's the combination of signal freshness, customer segmentation, and compliance posture. AI capability is the same for everyone; only the sellers who run those three things well survive 12 months.
