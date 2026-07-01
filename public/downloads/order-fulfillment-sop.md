# Order Fulfillment SOP — End to End

One pass: receive → procure → pack → ship → deliver → post-sale. Time budgets
in parentheses are realistic for a single-store / small-team setup, not a 3PL
running 5,000 orders/day.

## When to use

- First 90 days of a new store. Skip the optional steps until volume forces them.
- After onboarding a new 3PL or shipping carrier.
- When late-delivery rate > 8% or refund rate > 6% (excluding buyer's remorse).
- Quarterly: refresh thresholds against actual data.

## Stage 1 — Receive (T+0)

Within 15 minutes of order placement:

- [ ] Order auto-imported to OMS (Shopify, WooCommerce, custom).
- [ ] Address validated against carrier rules (USPS, Royal Mail, JNE etc.).
  Reject: PO box for UPS, missing postal code, unsupported region.
- [ ] Fraud check: order > 3× AOV from new email → manual review.
- [ ] Inventory reserved (decrement available, ignore pending).
- [ ] Customer confirmation email sent with delivery window, NOT a fixed date.

If order is fraud-flagged → hold; do not procure.

## Stage 2 — Procure (T+0 to T+1)

Three paths. Pick by lead time on the SKU:

| Lead time | Action |
|---|---|
| In stock | Pick from warehouse; do not touch supplier |
| 3–7 days | Drop-ship order to supplier (AliExpress, agent) immediately |
| > 7 days | Move to waitlist; refund if customer won't accept delay |

- [ ] Supplier order ID saved against the customer order ID. One row per SKU.
- [ ] Trackable link pushed back to the OMS within 24 hours of supplier confirmation.
- [ ] Customer notified if lead time slipped > 2 days vs. original promise.

What this stage does NOT do: it doesn't manage supplier contracts or reorder
thresholds. That's inventory planning.

## Stage 3 — Pack (T+1 to T+3)

- [ ] Pick list printed against available inventory.
- [ ] QC: every unit inspected for damage, missing accessories, wrong variant.
  Reject rate above 2% per batch → escalate to procurement, not customer service.
- [ ] Pack per shipping rule (weight, fragile, hazmat). Don't trust SKU weight
  metadata blindly — reweigh if size changed.
- [ ] Insert per A/B test plan. Track which insert each order received.
- [ ] Shipping label generated with carrier + service level. Service level
  chosen by SLA, not by lowest cost.

If you have > 200 orders/day, split packing by SKU group. Otherwise one queue
is fine.

## Stage 4 — Ship (T+3)

- [ ] Carrier pickup confirmed or drop-off receipt scanned.
- [ ] Tracking number pushed to OMS and customer email within 1 hour of label scan.
- [ ] Tracking number is one of the major aggregators (17track, AfterShip). Don't
  email a carrier-direct URL; carrier domains look like spam.
- [ ] "Shipped" notification includes: ETA range, support contact, return policy link.

Don't promise a delivery date. Promise a delivery window. Dates break on weather,
carrier exceptions, and holidays.

## Stage 5 — In transit (T+3 to T+ETA)

Two checks, no more. Automation handles the rest.

- [ ] Daily exception scan: orders stuck > 5 days with no scan → manual lookup.
- [ ] On T+7 (or 50% of ETA, whichever is earlier), if no delivery scan, send
  a proactive "still on the way" email. Reduces "where is my order" tickets by
  ~30%.

Stop here. Don't open carrier accounts to "check on the package" — that just
creates noise.

## Stage 6 — Delivered & post-sale (T+ETA)

- [ ] Delivery confirmation fires within 48 hours of carrier scan. If it doesn't,
  treat as "potentially lost" → start claim on day 7 post-ETA.
- [ ] Wait 7 days post-delivery, then send a 1-question review request. One
  question. Open-ended comment box optional.
- [ ] Returns: keep the policy short, the workflow obvious. Pre-printed return
  label = fewer "how do I return" tickets.
- [ ] Refund processed within 48 hours of return received, not of return requested.

## Time-budget summary

```
Receive      15 min    automation-heavy
Procure      ≤ 24 h    dropship order placed same shift
Pack         1–2 days  depends on inventory location
Ship         same day  before carrier cutoff
In transit   5–14 days carrier-controlled
Post-sale    ≤ 14 days review request fires
```

If any stage consistently blows its budget, the fix is process, not heroics.

## What this SOP does NOT cover

- Returns processing detail (refund timing yes; inspection/grading no).
- 3PL contract negotiation. Run after you've outgrown self-fulfillment.
- Customs paperwork for cross-border returns.
- Subscription / continuity billing. Different rules apply.
- Customer service scripts for complaints. This is the fulfillment layer.

## Source

Compiled from internal ops reviews across single-store and small-team setups,
2024–2026. Threshold numbers come from post-mortems on real orders, not vendor
SLAs.