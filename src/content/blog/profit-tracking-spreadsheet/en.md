---
title: 'How to Build a Cross-border Profit Tracking Spreadsheet'
description: 'Step-by-step tutorial for building a profit-tracking spreadsheet in Excel or Google Sheets. Includes formulas, dashboard setup, and free template link.'
pubDate: 2026-06-30
category: 'ops'
tags: ['excel', 'spreadsheet', 'profit', 'tracking']
translationKey: 'profit-tracking-spreadsheet'
tldr: 'A profit-tracking spreadsheet needs four sheets: orders, costs, ads, and a dashboard with SUMIFS formulas pulling net profit by product, channel and month.'
faq:
  - q: 'What columns should a profit tracking spreadsheet have?'
    a: 'Orders sheet: date, order ID, channel, SKU, quantity, sale price, currency, payment fee, shipping cost, product cost. Ads sheet: date, channel, campaign, spend, clicks, conversions, revenue. Dashboard sheet pulls totals via SUMIFS.'
  - q: 'How do I calculate profit in Google Sheets?'
    a: 'Net profit = revenue − product cost − shipping cost − payment fee − ad spend − refund cost. Use SUMIFS to sum each cost category by product, channel or month.'
  - q: 'Should I track profit by SKU or by order?'
    a: 'Both. Track by SKU to see which products are profitable; track by order to spot individual high-cost outliers (refunds, partial refunds, chargebacks).'
  - q: 'How often should I update my profit spreadsheet?'
    a: 'Daily for ads and orders (15 minutes). Weekly reconciliation with bank/payment processor (1 hour). Monthly review of net profit by product (2 hours).'
  - q: 'Is Google Sheets or Excel better for ecommerce tracking?'
    a: 'Google Sheets wins for collaboration and free access. Excel wins for power (Power Query, pivot tables, Power BI integration). For solo sellers, Google Sheets is enough.'
---

Most sellers track revenue but not profit. Profit is what you actually keep. Here's how to build a spreadsheet that tells the truth.

## The four sheets you need

A complete profit tracker has four sheets:

### 1. Orders (the input)

Every sale gets one row.

| Column | Description |
|---|---|
| date | Order date |
| order_id | Unique order ID |
| channel | Shopify, Etsy, Amazon, etc. |
| sku | Product identifier |
| qty | Quantity sold |
| sale_price | Per-unit price |
| currency | USD, EUR, GBP |
| payment_fee | What Stripe/PayPal took |
| shipping_cost | What you paid for shipping |
| product_cost | Supplier cost (allocated) |
| shipping_country | Destination country |
| customer_email | For repeat customer analysis |
| status | paid, refunded, partially_refunded |
| refund_amount | If refunded |
| chargeback_flag | TRUE/FALSE |
| notes | Anything noteworthy |

### 2. Costs (the input)

Per-order costs that vary.

| Column | Description |
|---|---|
| date | Cost date |
| type | shipping, packaging, label, customs, duty, etc. |
| amount | Cost |
| related_order_id | Order ID if applicable |
| notes | Context |

### 3. Ads (the input)

Daily ad spend and result data.

| Column | Description |
|---|---|
| date | Spend date |
| channel | Google, Meta, TikTok, Pinterest |
| campaign | Campaign name |
| spend | Daily spend |
| clicks | Clicks |
| conversions | Conversions (from platform) |
| conversion_value | Revenue attributed (from platform) |

### 4. Dashboard (the output)

Pulls from the other three sheets via formulas. Update it once, see everything.

## Key formulas

### Total revenue by month

```
=SUMIFS(Orders!F:F, Orders!A:A, ">="&DATE(2026,1,1), Orders!A:A, "<"&DATE(2026,2,1))
```

### Net profit by product (last 30 days)

```
=SUMIFS(Orders!F:F, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!I:I, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!H:H, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!G:G, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30)
```

Where F is revenue, I is product cost, H is shipping cost, G is payment fee.

### Net margin %

```
=net_profit_cell / total_revenue_cell
```

### ROAS by channel (last 30 days)

```
=SUMIFS(Ads!F:F, Ads!B:B, "Google", Ads!A:A, ">="&TODAY()-30) /
 SUMIFS(Ads!D:D, Ads!B:B, "Google", Ads!A:A, ">="&TODAY()-30)
```

### Ad-driven profit per order (Google, last 30 days)

```
=(SUMIFS(Ads!F:F, ...) / SUMIFS(Ads!E:E, ...)) -
 SUMIFS(Orders!I:I, ...) / COUNTIFS(...)
```

## Dashboard layout

```
┌─────────────────────────────────────────────────────────┐
│  CROSS-BORDER PROFIT DASHBOARD — Last 30 Days           │
├─────────────────────────────────────────────────────────┤
│  Revenue:           $X,XXX     ▲ X% vs prev 30d         │
│  Net Profit:        $XXX       ▼ X% vs prev 30d         │
│  Net Margin:        XX.X%                                │
│  Ad Spend:          $XXX       ROAS: X.X×                │
│  AOV:               $XX.X      Orders: XXX               │
├─────────────────────────────────────────────────────────┤
│  PROFIT BY SKU                                          │
│  SKU-001   $XXX   XX% margin   ████████████             │
│  SKU-002   $XXX   XX% margin   █████████                │
│  SKU-003   -$XX   -XX% margin  ██                       │
│  ...                                                    │
├─────────────────────────────────────────────────────────┤
│  PROFIT BY CHANNEL                                      │
│  Shopify  $XXX    Etsy  $XXX    Amazon  $XXX            │
├─────────────────────────────────────────────────────────┤
│  TOP EXPENSES (last 30d)                                │
│  Ad spend      $XXX  XX% of revenue                     │
│  Shipping      $XXX  XX% of revenue                     │
│  Payment fees  $XXX  XX% of revenue                     │
│  Product cost  $XXX  XX% of revenue                     │
│  Refunds       $XXX  XX% of revenue                     │
└─────────────────────────────────────────────────────────┘
```

## Implementation steps

1. **Create the four sheets** with headers above.
2. **Import orders daily** — Shopify, Etsy, Amazon all export CSVs. Use a script or manual import.
3. **Import ad spend daily** — Google Ads API, Meta API, or CSV export.
4. **Set up formulas** in the Dashboard sheet once. They update automatically.
5. **Add conditional formatting** — green for profit, red for loss on each row.
6. **Set up weekly email summary** — Google Sheets can email the dashboard as PDF.

## Common pitfalls

### Currency mixing

Don't mix USD and EUR in the same revenue column. Either:
- Convert all to USD at the date of sale (use daily exchange rate)
- Keep separate columns and convert at month-end

### Product cost allocation

If you sell bundles or multipacks, allocate cost per SKU. Don't put the full supplier cost on one SKU.

### Refund tracking

Refunds don't reverse your original cost. They add a new row in the Costs sheet with the refund amount as negative revenue.

### Returns without refunds

Some customers keep the product and get a partial refund. Track as a separate cost line, not as a refund.

### Ad spend attribution

Platform-reported conversions often disagree with your order data. Use platform-reported for ROAS, but reconcile with bank deposits monthly.

## Automating the data flow

### Shopify to Google Sheets

Use Shopify's API + Google Apps Script, or a tool like:

- **Matrixify** — bulk export/import
- **Shopify Google Sheets add-on** — direct sync
- **Zapier** — order → new row trigger

### Ads to Google Sheets

- **Google Ads API + Apps Script** — daily pull
- **Supermetrics** — paid, but reliable
- **Manual CSV export** — works for solo sellers at $10k/month

### Bank to Google Sheets

Most banks don't have direct integration. Manual weekly reconciliation is fine for small sellers.

## When you outgrow spreadsheets

At ~$50k/month revenue, you need:

- **Inventory tracking** — spreadsheets can't track stock in real time
- **Multi-currency** — multiple bank accounts, multiple supplier payments
- **COGS accuracy** — landed cost calculations per shipment
- **Channel-specific fees** — Amazon FBA storage, Etsy ads, etc.

Move to:

- **A2X + Google Sheets** — accounting layer over Shopify
- **QuickBooks Online** — basic but solid
- **Xero** — better for international
- **Cin7 or DEAR** — full inventory + accounting

For sellers under $50k/month, a well-maintained spreadsheet beats any of these.

## Get the template

Download our free [profit-tracking spreadsheet template](/resources/) — ready to use in Google Sheets or Excel.