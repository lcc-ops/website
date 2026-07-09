---
title: "A Google Sheet + auto-email reminder sold for $12/month to a local HVAC owner: why the boring AI plays in 2026 aren't in AI tools"
description: "Cold read of a $12/month Google Sheet + auto-email 'customer follow-up' product sold to a local blue-collar service business (HVAC). Mechanic: a Google Sheet tracks every install and auto-emails the owner when filters need swapping, warranties are about to lapse, or 6-month service is due. The case is not about the $12. The case is about the addressable market — local blue-collar service owners (plumbers, cleaners, landscapers, detailers) who still run follow-up in their head."
pubDate: 2026-07-09
category: 'ai'
tags: ['ai', 'automation', 'local-service', 'saas', 'case-study', 'monetization']
translationKey: 'local-services-ai-followup'
tldr: "A solo operator built a $12/month Google-Sheet-plus-auto-email 'customer follow-up' product for a local HVAC owner. The product reminds the owner when filters need swapping, warranties are about to lapse, or 6-month service is due. The product now runs at $24/month across two shops. The case is not about the $24. The case is about the addressable market — local blue-collar service owners (plumbers, cleaners, landscapers, detailers) who still run follow-up in their head and lose repeat revenue because of it. The leverage is not the AI; the leverage is the reminder."
faq:
  - q: "What is the product?"
    a: "A Google Sheet tracking every customer install, plus an auto-email that fires reminders to the owner (not the customer) on schedule: 3-month filter swap, near-warranty-expiry, 6-month service due. The product is sold for $12/month to one HVAC shop, now $24/month across two shops."
  - q: "Why does a $12/month product matter?"
    a: "It doesn't, on its own. The structural point is the addressable market: every local blue-collar service business (plumber, cleaner, landscaper, detailer, pest control, appliance repair) runs follow-up in the operator's head. The number of such businesses in the US alone is in the millions. A $12/month product with low churn, sold shop-by-shop via local relationships, scales to $10K–$50K/month at single-shop margins."
  - q: "What does the operator actually do?"
    a: "Three things, on repeat: (1) visit a local shop, offer a 30-day free trial; (2) help the owner import past customers into the sheet; (3) tune the reminder schedule to the shop's service pattern. The AI role is minimal — auto-email and a basic spreadsheet. The human role is the local relationship and the tuning."
  - q: "What is the unit economics?"
    a: "Per shop: $12/month revenue. Operator cost to onboard: 2–3 hours (visit, import, tune). Operator cost to maintain: ~30 minutes per month (handle edge cases, follow up on churn risk). At 50 shops: $600/month revenue, 25 hours/month of maintenance, effective gross of ~$24/hour. At 200 shops: $2,400/month, 50 hours/month, effective gross ~$48/hour."
  - q: "Why hasn't this been productized already?"
    a: "Three reasons. (1) Local relationships are slow and not VC-fundable. (2) The product is too small per shop to be worth a SaaS company's CAC math. (3) The trust barrier is high — a service owner won't install a 'CRM' from a stranger, but will sign up for a 'Google Sheet your tech guy set up'. The product is wrapped as a service, not as software."
  - q: "What does the case quietly skip?"
    a: "Four gaps. (1) Churn rate — the case does not name a churn number. Local shops that stop using the sheet typically do so within 6 months. (2) Sales CAC — the case implies relationship-based sales but does not name the close rate or cost per signed shop. (3) Tax / bookkeeping overhead — $12/month from 200 shops means 200 small Stripe transactions plus local sales tax in some US states, which quietly consumes margin. (4) Competitive risk — ServiceTitan, Housecall Pro, Jobber already ship similar reminders; the case does not address why a shop would pay $12/month to a stranger when the existing field-service software offers the reminder as a bundled feature."
---
A case profiles a solo operator who built a Google-Sheet-plus-auto-email 'customer follow-up' reminder product for a local HVAC (heating, ventilation, air conditioning) shop owner. The product tracks every install the shop has done, then auto-emails the owner (not the customer) when a 3-month filter swap is due, when a warranty is about to lapse, or when a 6-month service check is due. The product sells for $12/month. The operator signed a second shop; the product now runs at $24/month across two shops. The case frames the lesson not as 'the $24' but as the addressable market — local blue-collar service business owners who still run follow-up in their head and lose repeat revenue because of it.

The structural claim is that the AI-tools market in 2026 is saturated, but the AI-leveraged local-service market is not. The product is not the AI. The product is the reminder, sold to a non-technical buyer in a face-to-face relationship. The AI is the auto-email — the cheapest possible piece of the stack. Below is the per-shop economics, the addressable market, and four gaps the case does not address.

## The product

```
Customer install logged in Google Sheet
   (date, equipment, customer contact, install notes)
   ↓
Scheduled reminder rules:
   - 3 months: filter swap due
   - 11 months: warranty about to lapse (1 month buffer)
   - 6 months: standard service interval
   ↓
Auto-email fires to the owner:
   "Job #N customer — filter swap due — call to book"
   ↓
Owner calls customer, books the job
```

The product is, mechanically, a Google Sheet plus a scheduled auto-email. There is no model, no agent, no app. The edge is not the AI. The edge is the reminder that previously lived in the owner's head and was forgotten.

## Per-shop unit economics

| Item | Value | Notes |
|---|---|---|
| Price per shop | $12/month | Case-quoted |
| Onboarding operator cost | 2–3 hours | Visit, import past installs, tune schedule |
| Monthly maintenance | ~30 minutes | Edge cases, churn-watch |
| Net per shop (at scale) | ~$10/month | After Stripe fees, time allocation |
| Churn (assumed) | ~10%/month | Typical local SaaS pattern |
| Months to recover onboarding | 2–3 months | At $10 net, $20–30 onboarding cost |

The economics per shop are thin. The economics across many shops are the point.

## The addressable market

The structural argument is the number of shops the operator can sign, not the per-shop revenue.

```
US local blue-collar service businesses:
  - HVAC shops:                       ~120,000
  - Plumbing shops:                   ~130,000
  - Cleaning services:                ~60,000 (commercial)
  - Landscaping:                      ~100,000
  - Auto detail:                      ~50,000
  - Pest control:                     ~30,000
  - Appliance repair:                 ~40,000
  - Total addressable (rough):        ~500,000 shops
```

At a 1% signup rate (5,000 shops) the operator runs a $60,000/month business at a single-shop price. The math is not exciting, but it is real. The point is that the addressable market is not 'AI buyers' — it is local service owners who lose repeat revenue to memory failure.

## Why this works when AI-tool SaaS does not

Three reasons.

1. **The product is wrapped as a service, not software.** A service owner will not 'install a CRM'. A service owner will sign up for 'a Google Sheet your tech guy set up for me'. The human-relationship wrapper does the work that a SaaS landing page cannot.
2. **The CAC is local, not digital.** The operator walks into shops, sets up the product, and gets the signup in person. CAC is the cost of an afternoon of local visits, not the cost of a Google Ads campaign.
3. **The buyer is non-technical, and the price is non-threatening.** $12/month does not require procurement approval. The owner swipes a personal card and forgets about it. AI SaaS at $99/month requires a credit card the owner shares with their accountant.

The structural lesson is: in 2026, the AI tools market is saturated; the AI-leveraged local-services market is not. The competition for the latter is ServiceTitan, Housecall Pro, Jobber — but those products are priced at $200–$500/month and require a multi-day onboarding. A $12/month Google Sheet sold by a person over a cup of coffee is not in their market.

## What the case does not cover

Four gaps.

1. **Churn rate.** The case does not name a churn number. Local shops that stop using the sheet typically do so within 6 months — either the owner forgot the value, the operator moved on, or a competing field-service software bundled the reminder in. A 10%/month churn number is plausible but unconfirmed.
2. **Sales CAC and close rate.** The case implies a relationship-based sale but does not name the close rate. If the operator visits 50 shops and signs 5, the CAC is 10 visits per signup. If the operator visits 50 and signs 25, the math is fundamentally different.
3. **Tax and bookkeeping overhead.** $12/month from 200 shops means 200 small Stripe transactions plus local sales tax in some US states. The bookkeeping overhead quietly consumes margin and the operator's time. The case does not address this.
4. **Competitive risk.** ServiceTitan, Housecall Pro, Jobber all already ship similar reminders. The case does not address why a shop would pay $12/month to a stranger when their existing field-service software offers the reminder as a bundled feature at no marginal cost. The answer — that those products are over-featured and the local relationship is the real product — is plausible but not stated.

## Take-away

The case is not 'a Google Sheet made $24/month'. The case is: a $12/month product, sold shop-by-shop in a local relationship, scales to a real business because the addressable market (local blue-collar service businesses running follow-up in their head) is in the millions. The AI role is the auto-email. The edge is the reminder.

For most operators reading this case, the bottom line is: stop building AI tools. Walk into 10 local shops in your town. Offer to set up a Google Sheet reminder system for $12/month. The product takes an afternoon to build. The relationship is the moat. The repeat revenue compounds shop by shop.
