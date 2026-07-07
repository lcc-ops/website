---
title: "Medvi: 2 people, 400M USD in 15 months, and the 'own the customer, lease the rest' model behind the curve"
description: "Cold read of Medvi (Matthew Gallagher): 2-person remote-health company doing 400M USD in sales on 250k customers in year one, scaling toward 1.8B USD, 16.2% net margin vs Hims at 5.5% with 2,442 staff. The structural claim: the company is not a healthcare company — it is a customer-acquisition and experience layer on top of rented infrastructure."
pubDate: 2026-07-07
category: 'ai'
tags: ['ai', 'health', 'one-person', 'infrastructure', 'pricing', 'case-study', 'monetization']
translationKey: 'medvi-one-person-clinic-layer'
tldr: "Medvi (Matthew Gallagher) reportedly did 400M USD in sales on 250k customers in 15 months with a 2-person team, scaling toward 1.8B USD. Net margin 16.2%, versus Hims and Hers at 5.5% with 2,442 staff. The structural observation: Medvi does not employ doctors, hold pharmacy licenses, run logistics, or build infrastructure. It owns brand, distribution, and customer relationships, and leases everything else — clinical delivery to licensed third-party platforms, fulfillment to pharmacy service vendors, support to AI + voice synthesis. A 3,000–12,000 USD/year AI tool stack replaces what would cost 130,000+ USD in headcount. The moat is owning the customer relationship, not owning the operational stack."
faq:
  - q: "What is Medvi actually?"
    a: "A US remote-health company selling prescription weight-loss and related treatments direct-to-consumer. It runs paid acquisition, branding, and customer relationships in-house. Clinical consultations are delivered by licensed physicians through a third-party telehealth platform. Pharmacy fulfillment is outsourced. Customer support is delivered through an AI agent plus voice synthesis. Two-person team: the founder and his brother."
  - q: "What is the headline revenue number?"
    a: "Reported: 400M USD in sales between September 2024 launch and end of 2025 — roughly 15 months — on 250,000 customers. 2026 is reportedly tracking toward 1.8B USD. Net margin 16.2%. Hims and Hers Health, the closest public comparable, runs roughly 2.4B USD revenue with 2,442 employees and a 5.5% net margin. Medvi's revenue-per-employee is orders of magnitude higher."
  - q: "What does Medvi own, and what does it lease?"
    a: "Owns: brand, paid-acquisition funnel, customer relationships, customer data, retention / upsell motion. Leases: licensed physicians via a third-party telehealth platform, pharmacy fulfillment and logistics, customer support (AI + voice synthesis), payment rails, KYC / compliance. The 'lease everything else' pattern is what keeps the team at two people."
  - q: "Why does the leased-infrastructure model produce higher margin?"
    a: "Three reasons. (1) Variable cost: clinical and fulfillment scale with revenue, not headcount. (2) No capex: no clinics, no pharmacy licenses, no fulfillment centers. (3) AI tool stack substitution: an AI tool stack costing 3,000–12,000 USD/year replaces 130,000+ USD in equivalent headcount. The 3–10x cost gap is what makes 16.2% net margin achievable on a small team."
  - q: "What is the failure mode?"
    a: "The case names one directly: AI customer support hallucinated drug pricing and invented product lines that did not exist. The founder absorbed the cost. The lesson: AI output touching money or customer promises needs a human-review layer, even when the AI is the cost-saving play. Saving on the review layer is the place the case explicitly says not to save."
  - q: "What does the case quietly skip?"
    a: "Four gaps: (1) regulatory risk on the leased clinical infrastructure — telehealth licensing varies state-by-state, and the case gives no signal on Medvi's compliance posture; (2) paid-acquisition saturation — the curve is gated on Meta / Google / TikTok ad economics; CAC inflation in the GLP-1 category has already moved 30–50% year-over-year; (3) churn on cash-pay prescription customers — weight-loss customers churn at 40–60% within 6 months in comparable categories; (4) the 1.8B USD projection — self-attributed, not audited, and the 400M USD base year had unusually favorable tailwinds."
---

A knowledge-planet case profiles Matthew Gallagher's Medvi: a US remote-health company that reportedly hit 400M USD in sales on 250,000 customers in 15 months with a 2-person team, tracking toward 1.8B USD in 2026. The structural claim the case lands on is not "AI replaced the doctors" — it is "Medvi is not a healthcare company. It is a customer-acquisition and experience layer that sits on top of rented healthcare infrastructure." Below is the math, the leased-stack model, and four gaps the case does not address.

## What the case lays out

| Quantity | Value |
|---|---|
| Founder | Matthew Gallagher, 41, LA |
| Co-founders | 1 (his brother) |
| Total team | 2 |
| Launch | Sep 2024 |
| Reported sales (year 1) | 400M USD |
| Reported customers | 250,000 |
| 2026 trajectory | 1.8B USD (self-reported projection) |
| Net margin | 16.2% |
| Comparable: Hims and Hers | 2.4B USD revenue, 2,442 employees, 5.5% net margin |
| Product focus | Cash-pay prescription weight-loss, direct-to-consumer |

The case treats the team-size-to-revenue ratio as the load-bearing proof point, not the headline revenue number itself.

## What Medvi owns vs leases

The structural distinction the case draws:

```
Owns (in-house):
   brand
   paid-acquisition funnel (Meta / Google / TikTok ads)
   customer relationships and CRM
   customer data and LTV model
   retention and upsell motion
   packaging and presentation

Leases (third-party):
   licensed physicians (telehealth platform)
   pharmacy fulfillment and shipping
   customer support (AI agent + voice synthesis)
   payment rails
   KYC / identity verification
   compliance and adverse-event reporting
```

A full-stack telehealth company would own all of the leased items — clinical staff, pharmacy infrastructure, support team, fulfillment. Medvi owns none of them. The "own the customer, lease everything else" pattern is what keeps headcount at two.

## Why this model produces 3x the margin

Hims and Hers Health — the closest public comparable — runs roughly 2.4B USD revenue with 2,442 employees and a 5.5% net margin. Medvi reportedly runs 16.2% net margin on a 2-person team. The margin gap is not a function of being smaller; it is a function of cost structure:

| Line item | Full-stack telehealth | Medvi |
|---|---|---|
| Clinical staff | salaried physicians, ~200k USD/year × N | leased per-consult, variable with revenue |
| Pharmacy | owned licenses, fulfillment centers | leased per-fill, variable with revenue |
| Support | in-house team, ~40k USD/year × N | AI + voice synthesis, ~5–10k USD/month |
| Capex | clinics, license fees, fulfillment build-out | zero |
| Tool stack | per-employee tooling | AI tools at 3,000–12,000 USD/year replace 130,000+ USD headcount |

The 3–10x cost gap on the support layer is what makes 16.2% net margin achievable on a small team. The clinical and pharmacy layers scale with revenue as variable cost, so headcount does not have to scale with revenue at all.

## The pricing anchor

The case points out that Medvi's pricing is anchored to labor cost, not to per-script dispensing fees. A US-based telehealth consultation that would cost the customer $80–150 USD if billed as a service runs roughly $30–60 USD as part of a Medvi subscription bundle. The customer compares the bundle to "going to a clinic" and judges it cheap. Medvi captures a margin because the marginal cost of a consultation, leased in, is closer to $5–15.

This is the same job-vs-feature pricing move Cognition / Devin makes — but for telemedicine consultations instead of software engineering. Both products land on the labor-cost line of the customer's P&L instead of the per-service billable line.

## The failure mode the case names

The case is unusually direct about one failure:

> AI customer support hallucinated drug pricing and invented product lines that did not exist. The founder absorbed the cost.

This is the only place the case names a real operational loss. The lesson it draws: AI output touching money or customer promises needs a human-review layer, even when AI is the cost-saving play. Saving on the review layer is the place the case explicitly says not to save.

## What the case does not cover

Four gaps:

1. **Regulatory risk on the leased clinical infrastructure.** US telehealth licensing is state-by-state. The case gives no signal on Medvi's compliance posture, the legal structure between Medvi and the third-party clinical platform, or what happens if the clinical platform loses a state license in a state Medvi serves.
2. **Paid-acquisition saturation.** The 400M USD curve is gated on Meta / Google / TikTok ad economics. CAC inflation in the cash-pay weight-loss category has moved 30–50% year-over-year. The case does not address what happens to the unit economics when CAC doubles.
3. **Churn on cash-pay prescription customers.** Comparable categories show weight-loss customers churn at 40–60% within 6 months. The case gives no 12-month cohort retention figure.
4. **The 1.8B USD 2026 projection.** Self-attributed, not audited. The 400M USD base year had unusually favorable tailwinds (GLP-1 demand, cash-pay willingness, low competitive density). The 2026 trajectory assumes those tailwinds persist.

## Take-away

The model is "own the customer, lease the rest." It produces 3–10x the gross margin of a full-stack operator on the same revenue, because most of the cost stack is variable with revenue rather than fixed in headcount. The AI tool layer is what makes the support function viable on a small team — without AI, the cost saving on customer support collapses back to hiring, and the model fails.

A buyer evaluating this case: the lesson is not "be a one-person health company." It is "decide what you own and lease the rest." Most service businesses own too much — they hire when they could lease, they build when they could rent. The AI substitution layer is what makes the leased-only model cost-effective at the bottom of the stack; without it, the math reverts to headcount math.

For most operators reading this case, the structural takeaway is: name three things you own (brand, customer relationship, distribution) and lease everything else. The AI tool stack replaces what would have been the bottom of a hire list. The model works only when the leased infrastructure is mature enough to rent — which is a US-specific condition, not a universal one.