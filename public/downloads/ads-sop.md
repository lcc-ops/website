# Ads Launch SOP — Meta / TikTok / Google

7 steps before you spend $1 on any ad account. Run this checklist for every new
campaign, not just at account creation.

## When to use

- New ad account, no history.
- New product line entering paid traffic.
- Post-iOS 14.5 rebuild (≥ 6 months in, pixels still drifting).
- After a > 30% CPM spike with no clear cause.

## Step 1 — Account hygiene

- [ ] Business Manager verified, 2FA on, payment method not the personal one.
- [ ] One ad account per business entity. Sharing PBMs across stores corrupts learning.
- [ ] Pixel / CAPI installed server-side, deduped via `event_id`.
- [ ] Conversions API events firing on the same events as the pixel.
- [ ] Events tested in the last 14 days; no `error_code` 1 / 3 / 100 in Events Manager.

If any of these fail, stop. Pixel drift is the silent killer of every test you'll
run later.

## Step 2 — Naming convention

Pick one. Use it everywhere: ad set name, UTM, creative filename, Slack note.

```
{YYYY-MM-DD}_{channel}_{objective}_{audience}_{creative-angle}_{lang}
```

Example: `2026-07-02_meta_purchase_broad_us_ugc-v1_en`

What this buys you:

- Filter by date in any reporting view.
- Spot the angle that worked two weeks later without opening the ad.
- Hand off to a media buyer without a 30-minute Slack thread.

## Step 3 — Event & conversion setup

- [ ] One primary event per campaign. "Purchase" only. Don't optimize for ATC and expect learning to find buyers.
- [ ] Aggregated event measurement priority set in Events Manager (web): 1=Purchase, 2=InitiateCheckout, 3=AddToCart, 4=ViewContent.
- [ ] Customer list uploaded for LAL. Required, not optional.
- [ ] Cap on daily budgets at the campaign level, not ad set — let learning distribute.

## Step 4 — Audience structure

Default structure per market:

| Level | Size | Source |
|---|---|---|
| Ad set 1 | Broad | Country, age, no interest stack |
| Ad set 2 | LAL 1% | Based on purchasers, last 90 days |
| Ad set 3 | Interest stack | 3–5 interests, narrow overlap |
| Ad set 4 | Retarget | 30-day site visitors + ATC no purchase |

Test budget 60% / 10% / 20% / 10%. Don't change this for two weeks. Let
learning exit before judging.

## Step 5 — Creative

3 angles × 2 formats × 2 hooks per launch. Total 12 assets before launch.

Angles:

- Demo (product in use, 0–8s hook).
- Social proof (UGC review compilation, 5–15s hook).
- Comparison (vs category leader or "before/after").

Hook rules:

- First 3 seconds: state the problem or show the result.
- No logo in the first frame. Brand recall tests show this consistently.
- Caption on, always. 80%+ of paid social is watched on mute.

## Step 6 — Budget & learning exit

- [ ] Daily budget per ad set ≥ 5× target CPA. Below this, learning never exits.
- [ ] 50 conversions per ad set per week to exit learning. If your AOV is low, you need higher budget; if AOV is high, you need more time.
- [ ] Don't edit an ad set during learning exit. Any edit resets the clock to 7 days.
- [ ] Cap at 2× target CPA. If CPA > 2× target after $200 spent, kill the ad set.

## Step 7 — Kill rules & scaling

Hard kill (stop now):

- ROAS < 0.5 after $300 spent.
- Frequency > 3.0 on retargeting.
- CTR < 0.5% after 50,000 impressions on prospecting.

Soft kill (rotate out, keep campaign):

- CTR < 1% on prospecting after 7 days.
- CPA between 1.2× and 2× target.
- CPM rose > 50% week-over-week with no audience change.

Scale (vertical only, not horizontal):

- Increase budget ≤ 20% per 48 hours.
- Duplicate winning ad set only after 14 days of stable CPA, change only one variable (audience, creative, or budget).

## What this SOP does NOT cover

- Creative production at scale. Run this SOP *after* the creative is built.
- Post-purchase email/SMS flows. Separate SOP.
- Brand-level creative testing framework. This is channel-level.
- Compliance with category-specific ad policies (alcohol, supplements, financial).
  Verify before launch.

## Source

Compiled from common launch mistakes logged in our internal ad reviews, 2024–2026.
Not vendor-provided.