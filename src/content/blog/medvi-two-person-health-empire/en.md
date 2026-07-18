---
title: 'Medvi case: how a 2-person telehealth company hit 400M USD sales in 16 months by owning customers and renting everything else'
description: 'Cold-eyed read of Medvi, a 2-person remote-health operator that cleared 400M USD in 16 months and 16% net margin while its 2,442-person competitor ran at 5.5%. The "own the customer, rent the rest" thesis, the AI tool stack math, and where the model breaks.'
pubDate: 2026-07-08
category: 'ai'
tags: ['ai', 'telehealth', 'medvi', 'solo-saas', 'outsourcing', 'case-study', 'monetization']
translationKey: 'medvi-two-person-health-empire'
tldr: 'Matthew Gallagher opened Medvi in September 2024 with 20K USD and zero employees. By end of 2025 the company had done 400M USD in sales with 250K customers, two people on payroll, and a 16.2% net margin. Competitor Hims and Hers has 2,442 employees, 2.4B USD in sales, and a 5.5% net margin. The thesis is not "AI replaces doctors" — it is "you can own a customer relationship for a fraction of the cost by renting the rest of the infrastructure."'
faq:
  - q: 'What is the actual revenue and headcount?'
    a: 'September 2024 founding capital: 20K USD. End of 2025: ~400M USD sales, ~250K customers, 2 employees (the founder and his brother), 16.2% net margin. 2026 trajectory: 1.8B USD sales. Competitor Hims and Hers has 2,442 employees, 2.4B USD sales, 5.5% net margin. Numbers are self-reported; no audited financials are public.'
  - q: 'What does Medvi actually own vs rent?'
    a: 'Owns: brand, distribution channels, customer relationship, ad creative, the AI-assisted customer support layer. Rents: licensed doctors via a third-party compliance platform, pharmacy fulfillment, last-mile delivery, payment processing, customer support overflow, AI tools (Claude / voice synthesis / coding assistants). The founder is the customer-acquisition and experience layer; the rest is outsourced infrastructure.'
  - q: 'How does the AI tool stack math work?'
    a: 'Per the case: a single-person AI tool stack runs 3,000-12,000 USD per year. The equivalent labor cost (one full-time junior operations person) starts at 130,000 USD per year in the US. The 10-40x cost gap is the moat — the operator pockets the spread, the customer pays less than the regulated alternative, and the rented infrastructure absorbs the licensing and compliance work.'
  - q: 'Why does the case say "this is not an AI-replaces-humans story"?'
    a: 'Because the value is in owning the customer relationship, not in cutting labor. The labor was already outsourced to licensed practitioners on a third-party platform. The AI cuts the cost of the customer-experience layer, not the cost of the medical layer. A solo operator who tried to "replace the doctors" would hit a regulatory wall; an operator who owns the customer and rents the doctors stays legal and runs a real margin.'
  - q: 'What is the indie operator lesson?'
    a: 'Decide what you own (brand, distribution, customer list, repeat relationship) and rent everything else (compliance, fulfillment, infrastructure, payment). Use AI to compress the cost of the layer you own. Price against the team cost you are replacing, not against the tool subscription you are paying.'
  - q: 'What does the case not cover?'
    a: 'It does not disclose ad spend, customer acquisition cost, or refund and dispute rate. The 16.2% net margin claim has not been audited. The case also does not address what happens when the third-party doctor platform raises prices, when the pharmacy partner misses a delivery, or when the FDA decides the AI customer-support layer is itself a regulated medical device.'
---

Matthew Gallagher opened Medvi in September 2024 with 20K USD and no employees. Sixteen months later the company had done 400M USD in sales, served 250K customers, paid two salaries, and posted a 16.2% net margin. The competitor (Hims and Hers) had 2,442 employees, 2.4B USD in sales, and a 5.5% net margin. The case argues the gap is not AI vs human; it is owning the customer vs owning the infrastructure. Numbers, math, and where the model breaks.

## The headline numbers, side by side

| Metric | Medvi (2-person) | Hims and Hers (2,442-person) |
|---|---|---|
| Founded | September 2024 | 2017 |
| 2025 sales | ~400M USD | ~2.4B USD |
| Customers served | ~250,000 | not disclosed in this case |
| Employees | 2 (founder + brother) | 2,442 |
| Net margin | 16.2% | 5.5% |
| 2026 trajectory | ~1.8B USD | not disclosed in this case |

Per-employee sales: Medvi at 200M USD/employee, Hims and Hers at ~1M USD/employee. A 200x gap that the case reads as "the headcount was not the asset — the customer relationship was." Numbers are self-reported; no audited statements are public.

## The "own vs rent" split

What Medvi owns:

- Brand and customer-facing identity
- Ad creative and distribution channels
- Customer relationship and repeat-purchase loop
- AI-assisted customer support layer
- Pricing and packaging

What Medvi rents:

- Licensed doctors via a third-party compliance platform
- Pharmacy fulfillment and last-mile delivery
- Payment processing
- Customer support overflow
- AI tools (Claude for content, voice synthesis for call center, coding assistants for product iteration)

The founder is the "customer acquisition and experience layer." The rest is infrastructure. The case argues that every line item in the "rent" column is a SaaS or service business with mature APIs, mature SLAs, and pricing that scales linearly. The "own" column is what produces the margin.

## The AI tool stack math

```
One-person AI tool stack (annual):
  Claude subscription         240 USD
  Voice synthesis (call center)   ~1,200 USD
  Coding assistant             240 USD
  Marketing / analytics tools  1,000 - 10,000 USD
  ----------------------------------------
  Total                       3,000 - 12,000 USD / year

Equivalent labor cost (1 US junior operations FTE):
  Base salary                 65,000 - 85,000 USD
  Benefits + taxes + office   45,000 - 60,000 USD
  ----------------------------------------
  Total                       130,000 - 145,000 USD / year
```

The 10-40x cost gap is the moat. The operator pockets the spread, the customer pays less than the regulated alternative, and the rented infrastructure absorbs the licensing and compliance work. The case point: the AI is not the product; the AI is the leverage that lets one person do the work of ten.

## Why "this is not an AI-replaces-doctors story"

The case is explicit: the doctors were never in-house. The medical labor was already outsourced to a third-party compliance platform. The AI compresses the cost of the **customer experience layer**, not the medical layer. A solo operator who tried to "replace the doctors" would hit an FDA / state-board wall; an operator who owns the customer and rents the doctors stays legal and runs a real margin.

The structural lesson is to look at any regulated industry and ask: which layer is licensed, and which layer is the relationship? Own the relationship, rent the license. The same shape works in legaltech (own the intake, rent the lawyers), accounting (own the workflow, rent the CPA), and education (own the curriculum sales, rent the teachers).

## The indie operator playbook

The case ends with a six-step list, compressed:

1. **Decide what you own.** Brand, customer list, repeat-purchase loop, distribution. These never get outsourced.
2. **Rent everything else.** Compliance, fulfillment, infrastructure, payment, even overflow customer support. Mature SaaS handles this; do not rebuild it.
3. **Use mature building blocks.** Payment, email, voice, AI tools — all have production-ready tiers. Assemble, do not build.
4. **Run ad creative as a test machine.** AI can produce 50-100 creative variants per day; run them as a portfolio, kill the losers, scale the winners.
5. **Price against headcount, not software.** The buyer anchor is the team they would have hired, not the 20 USD/month tool line.
6. **Keep a human review gate for anything touching money or the customer.** The case mentions a real failure: Medvi AI customer support once hallucinated drug prices and a non-existent product line; the founder ate the loss. The case says it explicitly: "the output touched money, so a human still has to be in the loop."

## What this case does not cover

- **Ad spend and CAC.** The 400M USD sales number says nothing about how much was spent on the ad side. A 16% net margin on 400M means about 64M USD in profit; if the ad budget was, say, 200M, the implied CAC is around 800 USD/customer, which is plausible for telehealth but is not in the case.
- **Refund and dispute rate.** Telehealth has higher refund and dispute rates than the case implies. Chargeback rates above 1% are a red flag; the case does not show this number.
- **Audit.** The 16.2% net margin is a self-reported figure. No audited statements.
- **Platform risk.** The third-party doctor platform, pharmacy partner, and payment processor are all dependencies. Any of them raising prices, missing deliveries, or pulling out hits Medvi's economics directly. The case does not address this.
- **Regulatory drift.** The case assumes the AI customer-support layer is not a regulated medical device. The FDA has not made that determination, and a future ruling could push the entire customer-experience layer into compliance scope.

## Take-away

The model works because the customer relationship is the only asset that compounds, and the rest of the value chain can be rented. A solo operator who identifies the relationship layer in any regulated industry, owns it, and rents everything else has a real shot at the same margin math Medvi posts — at a smaller scale. The 16% net margin is not the moat; the moat is that the operator did not have to hire anyone to capture it. AI is the lever; the structural choice is what to own.

## Source

This case is a paraphrased summary of publicly reported coverage of Medvi (Matthew Gallagher) and adjacent 2-person telehealth operator stories. Headline figures — 400M USD in 16 months, 250,000 customers, 2 employees, 16.2% net margin, 1.8B USD 2026 trajectory — are quoted as the source material reports them; none are independently audited by the editor. Comparisons to Hims and Hers Health use publicly disclosed company filings. Medical, regulatory and reimbursement claims (telehealth licensing, GLP-1 supply, AI customer-support scope) are not legal or medical advice and have not been independently verified. This post is commentary on a business model, not medical or financial guidance; consult a licensed professional for clinical, tax or investment decisions. If you can point to a specific original report we should credit, write to contact@kuajinglab.xyz.
