---
title: 'An AI illustration blogger built a four-month, 200k-follower matrix on a Coze workflow, and the unit economics of selling the workflow itself'
description: 'Cold read of a "图解万物 / 万物图鉴" style AI illustration account that reportedly crossed 200,000 followers across a matrix in four months. Production runs on a Coze workflow. The case monetizes two layers: platform creator-share and a 1,000+ RMB course that bundles the workflow. Below is the math, the asset-library shape, and what the case is silent on.'
pubDate: 2026-07-07
category: 'ai'
tags: ['ai', 'illustration', 'coze', 'workflow', 'monetization', 'case-study']
translationKey: 'x-coze-image-illustration-account'
tldr: 'An AI-illustration account (exemplified by "图解万物 / 万物图鉴") reportedly built a 200,000-follower cross-platform matrix in four months on the back of a Coze workflow, then monetized two layers: platform creator-share and a 1,000+ RMB course that bundles the workflow. The first layer is the headliner number, but the second layer — selling the workflow itself — is the one that survives algorithm shifts. The hard part is not generating one illustration; it is keeping a Coze workflow stable across thousands of runs while a niche template library expands.'
faq:
  - q: 'What does the account actually publish?'
    a: 'AI-generated illustrations in a consistent visual style, typically explaining a category of objects, animals, or abstract concepts. Early posts concentrate on cats and dogs — high-emotion subjects with broad appeal. The visual style is a flat, character-driven illustration format rather than photorealism. Each post follows the same template: subject, structured caption, single-image payoff.'
  - q: 'What is the production stack?'
    a: 'A Coze workflow stitches together a prompt template, an image-generation model call, a caption generator, and a post-format helper. The workflow is the asset, not any single prompt. Each new topic feeds the workflow; the workflow outputs the post. This is what differentiates a one-off AI illustrator from a 200k-follower operator.'
  - q: 'What are the two monetization layers?'
    a: 'Layer one: official creator-share revenue on the publishing platform (image-text format pays per view / per engagement). Layer two: a 1,000+ RMB course that bundles the Coze workflow, prompt templates, and posting cadence. Layer one is platform-dependent and algorithm-fragile. Layer two is platform-independent and tied to the operator''s workflow IP.'
  - q: 'How big is layer one in actual numbers?'
    a: 'At a 200k cross-platform follower base with a 5–15% post-engagement rate and an image-text creator-share rate of roughly 3–8 RMB per 1,000 views, monthly creator-share revenue runs 5,000–20,000 RMB across the matrix. This is meaningful as a single-operator income but not life-changing; the headline follower count overstates the layer-one cash.'
  - q: 'Why is the Coze workflow the asset, not the prompts?'
    a: 'A prompt template can be replicated in a day; a Coze workflow with stable parameter sets, fallback logic, retry behavior, and a topic-pipeline front-end cannot. The workflow encodes the operator''s accumulated decisions about which prompts to retry, which captions to regenerate, and how to handle model refusals. That is what sells for 1,000+ RMB in a course.'
  - q: 'What does the case quietly skip?'
    a: 'Four gaps: (1) the actual layer-one revenue — the case gives followers and views, not creator-share RMB; (2) refund / dispute rate on the paid course, which is a known issue with packaged AI-workflow courses on Chinese creator platforms; (3) sustainability of the matrix after the initial niche saturation — cats-and-dogs is a 3–6 month window before fatigue; (4) platform-policy risk on AI-image-only accounts, which has tightened in the past 12 months on most major Chinese creator platforms.'
---

An AI-illustration account (in the "图解万物 / 万物图鉴" mold) reportedly built a 200,000-follower cross-platform matrix in four months on the back of a Coze workflow, and monetizes two layers at once: official creator-share revenue and a 1,000+ RMB paid course that bundles the workflow itself. The headline number — 200k followers in 4 months — is the part that gets shared. The structurally interesting part is the second layer. Below is the math, the workflow shape, and what the case quietly skips.

## What the case claims

| Quantity | Value |
|---|---|
| Reported cross-platform followers | 200,000+ in 4 months |
| Initial niche | Cats and dogs (high-emotion, broad appeal) |
| Production tool | Coze workflow (prompt + image gen + caption + format) |
| Visual style | Flat, character-driven illustration, consistent across posts |
| Monetization layer 1 | Official creator-share on the publishing platform |
| Monetization layer 2 | 1,000+ RMB paid course bundling the Coze workflow |
| Matrix strategy | Cross-platform accounts running the same workflow |
| Reported total monthly revenue | Not disclosed |

The case treats the workflow as the asset and the followers as the marketing channel. The two layers are deliberately separated: layer one is algorithm-fragile, layer two is platform-independent.

## Why a Coze workflow is the asset, not a prompt

Three properties of a workflow distinguish it from a single prompt template:

1. **Stable parameter sets.** A workflow encodes which model to call, at which temperature, with which retry budget. A prompt template requires the operator to remember these. The workflow removes the memory dependency.
2. **Pipeline front-end.** A workflow that ingests a topic and outputs a finished post is a different product than a prompt that requires the operator to write the caption, format the post, and check the image. The pipeline converts "creative work" into "topic input."
3. **Failure handling.** A workflow with retry, fallback, and refusal logic absorbs model-version drift. A prompt copied from an old blog post breaks silently when the underlying model is updated. The operator whose workflow survives the model update keeps the income; the operator whose prompts drift loses the income.

This is why a packaged Coze workflow can sell for 1,000+ RMB. The buyer is paying for accumulated operator decisions, not for the model itself. The model is the cheap part.

## Cost structure and unit economics

```
Coze platform fee:                     free tier or 0–99 RMB/month
Image-generation model cost per post:   0.05–0.50 RMB (depending on model)
Per-post operator time:                5–15 minutes (topic input + review)
Posts per day (matrix-wide):           10–30 (across accounts)
Monthly tooling cost (model + Coze):   50–300 RMB
Monthly operator time:                 40–120 hours
```

At a 200k cross-platform follower base, creator-share revenue runs **5,000–20,000 RMB/month** depending on platform mix and engagement rate. Course sales are lumpy — a launch month can move 100–500 copies at 1,000+ RMB each, generating 100k–500k RMB in a single month, then taper to a maintenance rate of 10–30 copies/month as the niche matures.

Layer one funds the operator''s time. Layer two funds the operator''s business. The case mixes the two in a way that overstates layer one and understates layer two.

## The matrix is the distribution, not the moat

Cross-platform accounts running the same workflow are an attention-multiplication pattern, not a moat. The pattern works because:

- Each platform has its own audience pool; a 50k account on three platforms is 150k reach.
- Creator-share rates differ across platforms; the operator allocates output to whichever pays best per view.
- Workflow output is fungible across platforms; the marginal cost of the third platform is near-zero.

What the matrix cannot do is defend against workflow replication. A buyer of the 1,000-RMB course now has the same workflow. The matrix moat exists only while the niche is unfilled and the operator is the first mover.

## What the case does not cover

Four gaps:

1. **Actual layer-one revenue.** The case gives followers and views, not creator-share RMB. The two are weakly correlated — a 200k matrix with a 3% engagement rate on image-text posts pays materially less than the follower count suggests.
2. **Course refund / dispute rate.** Packaged AI-workflow courses on Chinese creator platforms have a documented pattern of disputes after the buyer fails to replicate the workflow. The case gives the price, not the dispute rate.
3. **Niche saturation.** Cats-and-dogs illustration is a 3–6 month window before the format fatigues. The case does not give the 12-month follower-curve.
4. **Platform-policy risk on AI-only accounts.** Most major Chinese creator platforms tightened AI-only-image policies in the past 12 months. The case gives no signal on labeling, disclosure, or platform-specific compliance posture.

## Take-away

If you can build the workflow before you build the audience, this model works. The two layers complement each other: layer one validates the niche, layer two extracts the durable value. If you build the audience first and the workflow second, you are running a content business, not a workflow business, and the matrix moat collapses within one platform-policy cycle.

A buyer picking this up: the headline follower count is the marketing layer, not the income layer. The Coze workflow is the asset; the course is the monetization; the followers are the funnel. Replicating the followers without replicating the workflow produces a different business with a much shorter half-life.