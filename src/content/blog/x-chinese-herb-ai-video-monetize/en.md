---
title: "AI-generated Chinese herbal medicine short videos: 36万 followers and 10万 RMB in cumulative revenue, and what the 'copy-able playbook' framing actually skips"
description: "A case profiles a Chinese operator running AI-generated Chinese herbal medicine short videos on Douyin / Xigua. 358K–368K followers, 100K+ RMB cumulative revenue split between Douyin's creator-share program and 橱窗 e-commerce (herbal tea, related SKUs). The model is sold as a copy-able playbook. The unit economics, the per-video production cost, the platform-share math, and the four gaps the playbook quietly elides, below."
pubDate: 2026-07-10
category: 'ai'
tags: ['ai', 'short-video', 'chinese-medicine', 'douyin', 'content-monetization', 'case-study', 'monetization']
translationKey: 'x-chinese-herb-ai-video-monetize'
tldr: "An AI short-video account on Chinese herbal medicine reaches 358K–368K followers and 100K+ RMB cumulative revenue, split between Douyin's creator-share program and 橱窗 e-commerce. The model is a vertical-niche content farm — script from a GPT / Claude pass, AI voice, AI or stock visuals, herbal-tea SKUs in 橱窗. The interesting part is not 'AI makes videos' — it is the niche choice (high demand, low saturation, evergreen) and the unit economics of a one-person content farm. The four gaps: refund rate, 橱窗 GMV vs revenue split, Douyin policy on AI medical content, account-cluster risk."
faq:
  - q: "What does the case actually document?"
    a: "An operator runs a Douyin / Xigua short-video account on Chinese herbal medicine. 358K–368K followers. Cumulative revenue 100K+ RMB, split between Douyin's creator-share program (播放分成) and 橱窗 e-commerce on herbal tea and related SKUs. The script, voiceover, and visuals are AI-generated. The model is sold as a copy-able playbook."
  - q: "What is the unit economics?"
    a: "Per video: GPT / Claude script pass (15 min), AI voice clone (5 min), stock or AI-generated footage (30 min), human polish + 橱窗 SKU tagging (30 min). Total 1.5 hours per video. Cadence 7–14 videos per week. Steady-state weekly operator time 12–25 hours. Cash cost: Claude Pro or GPT Plus 20 USD/month, AI voice 10–30 USD/month, 橱窗 SKU cost-of-goods roughly 30% of GMV. Douyin's creator-share program pays roughly 10–30 RMB per 10K views, depending on niche and completion rate. At 358K followers and an average 50K–200K views per video, the per-video creator-share payout is 50–600 RMB."
  - q: "Why does this niche work where other AI-content farms fail?"
    a: "Three reasons. (1) Evergreen demand — herbal medicine and wellness content has a multi-decade shelf life, unlike trending memes. (2) Search-driven traffic — a large share of views come from search and recommendation on 'what does this herb do', not from the follower feed. The account is search-discoverable. (3) High-intent e-commerce match — herbal tea, foot-soak sachets, and similar SKUs convert at 2–5% on 橱窗 because the audience self-selects. A generic AI-content farm on cooking or motivation has a 0.3–1% 橱窗 conversion."
  - q: "What is the revenue math?"
    a: "100K+ RMB cumulative is a multi-month figure, not a monthly run rate. The follower ramp from 0 → 358K typically takes 4–8 months at 7–14 videos per week. At a steady-state monthly creator-share of 3K–10K RMB and 橱窗 GMV of 10K–30K RMB with 30% net margin, the steady-state monthly net is 6K–19K RMB. The 100K+ cumulative figure is consistent with 6–12 months at that run rate."
  - q: "What is the risk?"
    a: "Four risks. (1) Douyin policy on AI medical content — Douyin has been tightening rules on medical claims in short videos since 2024. A 2026 policy tightening could deplatform the account or block 橱窗 SKU listings. (2) 橱窗 SKU compliance — herbal products with health claims fall under 广告法 and 医疗器械管理条例. A SKU that slips into medical-claim language gets pulled and the account gets a strike. (3) Content homogeneity — the AI-script pass produces similar scripts across accounts; Douyin's de-duplication is increasingly aggressive on near-duplicate content. (4) Account-cluster risk — operators running multiple accounts in the same niche get caught by device-fingerprint and writing-style clustering. A single ban cascades."
  - q: "What does the case skip?"
    a: "Four gaps. (1) The case says '100W+ cumulative' but does not show the monthly split between creator-share and 橱窗 net. The two revenue streams have very different margins and risks. (2) Refund rate on 橱窗 herbal SKUs is not disclosed; herbal-product categories typically see 8–15% refund rates. (3) Account age and ban history — the case does not say whether this is the first account or a replacement after a previous ban. (4) The script-prompt stack is not shown — the actual prompt engineering is the moat, and the case treats it as commodity."
---

A case profiles a Chinese operator running AI-generated short videos on Chinese herbal medicine. 358K–368K followers on Douyin / Xigua. Cumulative revenue 100K+ RMB, split between Douyin's creator-share program and 橱窗 e-commerce on herbal tea and related SKUs. The model is sold as a copy-able playbook. The interesting part is not 'AI makes videos' — it is the niche choice (high search demand, low saturation, evergreen) and the unit economics of a one-person content farm. The unit-economics breakdown, the search-driven traffic shape, and the four gaps the playbook quietly elides, below.

## The unit-economics breakdown

```
Per video:
  GPT / Claude script pass:    15 min
  AI voice clone:              5 min
  Stock or AI-generated clip:  30 min
  Human polish + 橱窗 SKU tag: 30 min
  Total:                       1.5 hours per video

Cadence:                       7–14 videos / week
Weekly operator time:          12–25 hours

Cash cost (monthly):
  Claude Pro or GPT Plus:      20 USD
  AI voice (ElevenLabs etc.):  10–30 USD
  Stock footage (optional):    0–20 USD
  Total:                       30–70 USD / month
```

The production cost per video is roughly 5–10 RMB in cash plus 1.5 hours of operator time. At a steady-state 10 videos per week, the operator commits 15 hours per week. The model is a one-person content farm — the operator's job is script direction and SKU selection, not filming.

## The revenue math, split by stream

```
Douyin creator-share (播放分成):
  Average views per video:     50K–200K
  Payout per 10K views:        10–30 RMB (niche-dependent)
  Per-video creator-share:     50–600 RMB
  Monthly (40 videos):         2K–24K RMB

橱窗 e-commerce:
  Herbal tea + related SKU
  Per-video GMV (mid-funnel):  250–750 RMB
  Monthly GMV (40 videos):     10K–30K RMB
  Net margin (after COGS 30%): 7K–21K RMB / month

Combined monthly net:          9K–45K RMB
Cumulative 100K+ in 4–8 months: consistent
```

The interesting split is the ratio. Creator-share is volume-driven — more videos, more views, more payout. 橱窗 is intent-driven — fewer videos but higher per-view revenue because the audience self-selects on search. The two streams scale differently. Creator-share hits a ceiling at niche saturation; 橱窗 scales with account authority.

## The search-driven traffic shape

A generic AI-content farm on cooking or motivation lives on the follower feed. The video dies in 24 hours; the next video has to re-earn reach. A herbal-medicine account lives on search and recommendation — 'what does 黄芪 do', 'can 枸杞 hurt you', 'is 茯苓 safe daily'. The search shelf life is 6–18 months. A video ranking for a herbal-medicine search query keeps pulling views 12 months after publish.

The compounding effect: 358K followers is the visible number; the actual traffic is search-driven and 2–5x the follower feed. The operator's revenue per video does not collapse after the launch window the way a meme-content account does.

## What this case does not cover

- **The split between creator-share and 橱窗 net is not shown.** The 100K+ cumulative mixes a volume-driven stream (low margin, low risk) and an intent-driven stream (higher margin, SKU-compliance risk). A reader cannot tell which stream is the load-bearing one.
- **Refund rate on 橱窗 herbal SKUs.** Herbal-product categories on Douyin 橱窗 typically see 8–15% refund rates, driven by 'taste bad', 'no effect', and 'wrong SKU'. A 12% refund rate cuts the 橱窗 net by 12% before any other cost.
- **Account age and ban history.** The case does not say whether this is the first account or a replacement after a previous ban. A reader replicating the playbook should expect to lose 1–2 accounts to policy violations before the surviving account reaches scale.
- **The script-prompt stack.** The actual moat is the prompt engineering — the system that turns '黄芪 + 气血 + 副作用' into a 60-second video script that does not trip Douyin's medical-claim filter. The case treats the prompt stack as commodity; it is not. A commodity prompt stack produces commodity scripts that get de-duplicated by the platform within 4–8 weeks.

## Bottom line

The model is real: 358K followers, 100K+ cumulative, 6–12 months to scale. The niche choice is the load-bearing decision — evergreen demand, search-driven traffic, high-intent e-commerce match. A reader replicating the playbook should plan for 1–2 lost accounts, a 12% 橱窗 refund haircut, and a non-trivial prompt-engineering effort. Treat the cumulative 100K+ as a 6–12 month achievement, not a monthly run rate. The monthly run rate at scale is 9K–45K RMB, and that is the realistic steady-state for a one-person content farm.