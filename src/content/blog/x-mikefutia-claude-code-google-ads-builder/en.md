---
title: 'One URL to a launch-ready Google Search campaign: a read of a Claude Code Google Ads builder, with the unit economics behind it'
description: 'A high-engagement X post (619 likes, 526 replies) walked through a Claude Code build that takes one URL and outputs a complete Google Search campaign — keywords, ad groups, headlines, negatives, structured the way a paid-search agency would structure it. A read of what the build actually does, the per-campaign unit economics, and where the wrapper business sits.'
pubDate: 2026-07-23
category: 'ai'
tags: ['ai', 'google-ads', 'claude-code', 'agency-tool', 'case-study', 'monetization']
translationKey: 'x-mikefutia-claude-code-google-ads-builder'
tldr: 'A Claude Code build turns one URL into a complete, launch-ready Google Search campaign — keywords, ad groups, every headline, the negative list — structured the way a paid-search agency would structure it. The build collapses 6–10 hours of agency work into minutes and runs on a Claude subscription. The wrapper business sits at $200–800 per campaign delivered, with a built-in moat against the do-it-yourself buyer who has the technical skill but not the hours. The case is silent on the QA loop, the policy-review pass, and the conversion-tracking wiring that decide whether the campaign actually performs.'
faq:
  - q: "What does the Claude Code Google Ads builder do?"
    a: 'It takes one URL as input. It crawls the landing page, extracts the offer, the value proposition, the proof points, and the price. From those it generates a Google Search campaign structure: keyword themes grouped by intent, 15–30 headlines per ad group, 4 descriptions per ad group, a negative-keyword list, and ad-group-level bid recommendations. Output is a Google Ads Editor CSV that can be uploaded directly.'
  - q: "How long does the build actually take?"
    a: 'The Claude Code generation runs in 5–15 minutes per campaign. The remaining work — human QA on the headlines (cutting redundant ones, fixing any trademark or policy issue), conversion-tracking wiring, and the post-launch bid-tuning pass — takes another 2–4 hours of operator time. Total operator time per campaign is 3–5 hours, down from 6–10 hours for a manual agency build.'
  - q: "What does it cost to deliver?"
    a: 'Claude subscription is roughly $20–200/month per operator depending on the plan. Per-campaign Claude API cost is $2–8 in input tokens plus $5–20 in output tokens for the long campaign-generation prompt. Operator time is 3–5 hours at the operator''s hourly rate. Total cost to deliver one campaign is roughly $40–120 in tool spend plus operator time. At a $500 delivery price, gross margin is 60–80% before customer acquisition.'
  - q: "Who is the buyer?"
    a: 'Three profiles. (1) Small e-commerce merchants with $10k–100k/month ad spend who want a faster iteration loop than an agency provides. (2) Performance-marketing consultants who deliver 20–50 campaigns per quarter for their own clients and want to compress the per-campaign time. (3) Marketing teams at SaaS startups who run paid-search in-house but want to skip the first-draft work.'
  - q: "Where does the business make money?"
    a: 'Three places. (1) Direct delivery: $300–800 per campaign, billed per project or as a monthly retainer for 4–10 campaigns. (2) White-label delivery: the same build sold to agencies at $100–300 per campaign, with the agency re-billing the client at full agency rate. (3) Template resale: a curated campaign-template library at $50–200/month per subscriber.'
  - q: "What does the case leave out?"
    a: 'Four gaps. (1) The QA loop — every generated headline needs a human pass for trademark, policy, and brand-voice fit. The post does not name the rejection rate. (2) The conversion-tracking wiring — a Google Ads campaign without proper GA4 conversion events will not optimize correctly, and that wiring is not in the build. (3) The post-launch tuning — keyword pruning, bid adjustment, search-term-report review — is 4–8 hours of weekly work per active campaign and is not in the build. (4) The Google Ads policy review — generated headlines frequently hit trademark or "unrealistic claims" rejections that require manual rewriting. The case is silent on all four.'
---

A high-engagement X post (619 likes, 526 replies) walked through a Claude Code build that takes one URL and outputs a complete Google Search campaign — keywords, ad groups, every headline, the negative list — structured the way a paid-search agency would structure it. What follows is a read of what the build actually does, the per-campaign unit economics, and where a wrapper business around this build would sit.

## What the build does

| Stage | Input | Output | Time |
|---|---|---|---|
| Crawl + extract | One URL | Offer, value prop, proof points, price | 1–3 min |
| Keyword themes | Extracted offer | 5–12 ad groups by intent | 2–4 min |
| Headlines + descriptions | Ad groups | 15–30 headlines + 4 descriptions per ad group | 3–8 min |
| Negatives + bids | Ad groups | Negative-keyword list, bid recommendations | 1–3 min |
| Editor CSV | All of the above | Google Ads Editor import file | <1 min |

The build outputs a Google Ads Editor CSV that an operator can upload directly. The first-draft work is done. The remaining work is QA, conversion-tracking wiring, and post-launch tuning.

## Per-campaign unit economics

| Line item | Cost | Notes |
|---|---|---|
| Claude subscription | $20–200/month fixed | Amortize across 10–40 campaigns/month |
| Per-campaign API tokens | $7–28 | Input + output tokens for the long campaign-generation prompt |
| Operator time | 3–5 hours | QA, conversion tracking, launch |
| Customer-acquisition cost | $30–150 per customer | Cold outreach, paid ads, referral |
| **Total cost to deliver** | **$60–380** | Before operator hourly rate |

At a $500 delivery price, gross margin is 24–88% depending on operator efficiency and CAC. At $800, gross margin is 53–90%. The high end of the margin range requires the operator to be running 10+ campaigns per month to amortize the Claude subscription and the QA overhead.

## Who buys this

Three profiles, with different price sensitivity:

1. **Small e-commerce merchants ($10k–100k/month ad spend).** They want a faster iteration loop than an agency provides. Price tolerance is $300–800 per campaign, with a 4–10 campaign monthly retainer.
2. **Performance-marketing consultants.** They deliver 20–50 campaigns per quarter for their own clients and want to compress per-campaign time. Price tolerance is $100–300 per campaign as a white-label input they re-bill at full agency rate ($1,000–3,000 per campaign).
3. **SaaS marketing teams.** They run paid-search in-house but want to skip first-draft work. Price tolerance is $200–500 per campaign, with internal budget approval.

The three buyer profiles imply three different go-to-market motions: direct-to-merchant content marketing, agency partnerships, and SaaS community distribution. None is automatic.

## Where the wrapper business sits

Three viable shapes:

1. **Direct delivery.** $300–800 per campaign, billed per project or as a monthly retainer for 4–10 campaigns. Best fit for the small e-commerce buyer.
2. **White-label delivery.** The same build sold to agencies at $100–300 per campaign, with the agency re-billing the client at full agency rate. Best fit for the consultant buyer; the agency captures the margin and the operator captures volume.
3. **Template resale.** A curated campaign-template library at $50–200/month per subscriber. Best fit for the SaaS marketing-team buyer; the buyer self-serves from templates the operator has already QA'd.

The three shapes can be run in parallel from a single Claude Code build. The build is the same; the go-to-market and the price are different.

## What the case leaves out

The post shows the build running in minutes. The work that decides whether a campaign actually performs is missing from the post:

1. **The QA loop.** Every generated headline needs a human pass for trademark, policy, and brand-voice fit. Standard rejection rate is 10–30% of generated headlines. The post does not name this.
2. **Conversion-tracking wiring.** A Google Ads campaign without proper GA4 conversion events will not optimize correctly. The wiring is not in the build and is 1–3 hours of operator work per campaign.
3. **Post-launch tuning.** Keyword pruning, bid adjustment, search-term-report review is 4–8 hours of weekly work per active campaign. This is where the campaign actually wins or loses.
4. **Google Ads policy review.** Generated headlines frequently hit trademark or "unrealistic claims" rejections that require manual rewriting. Standard rewrite rate is 5–15% of generated headlines.

The build collapses the first-draft work. The work after the first draft is what makes the campaign perform. The case sells the build; the business is the post-launch tuning.

## Bottom line

A Claude Code Google Ads builder is a real product with three viable wrapper businesses around it. The build compresses 6–10 hours of agency work into minutes; the remaining 3–5 hours of operator work per campaign is the actual product. The wrapper margin is healthy at $500+ delivery prices; the moat against the do-it-yourself buyer is the QA + conversion-tracking + post-launch tuning loop, not the build itself.