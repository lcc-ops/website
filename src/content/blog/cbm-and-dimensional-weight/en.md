---
title: 'CBM and Dimensional Weight Explained (with Calculator)'
description: 'How to calculate CBM, chargeable weight and dimensional weight for air, sea and express shipping. Includes a free calculator and worked examples for common product sizes.'
pubDate: 2026-06-29
category: 'shipping'
tags: ['cbm', 'shipping', 'dimensional-weight', 'logistics']
translationKey: 'cbm-and-dimensional-weight'
tldr: 'CBM (cubic meter) = length × width × height in meters. Dimensional weight = (L × W × H in cm) ÷ 5000 for air/express, ÷ 6000 for sea. Carrier charges the greater of actual or dimensional weight.'
faq:
  - q: 'How do I calculate CBM for a shipment?'
    a: 'CBM = length × width × height, all in meters. For multiple boxes, calculate each box''s CBM and sum them. Example: 0.5m × 0.4m × 0.3m = 0.06 CBM.'
  - q: 'What is dimensional weight vs actual weight?'
    a: 'Actual weight is what the scale shows. Dimensional weight (volumetric weight) is (L × W × H in cm) ÷ 5000 for air/express, ÷ 6000 for sea. The carrier charges whichever is higher.'
  - q: 'What is the dimensional weight divisor for FedEx, UPS, DHL?'
    a: 'FedEx and DHL use 5000 (cm/kg) for international express. UPS uses 5000 for international and 6000 for domestic. USPS uses 194 (inches/pound) = 9000 (cm/kg) for First-Class packages.'
  - q: 'How much does it cost to ship 1 CBM by air?'
    a: 'For a 100kg+ shipment: $4–8/kg from China to the US. Below 100kg, dimensional weight usually applies, costing $6–12/kg of chargeable weight.'
  - q: 'When should I switch from air to sea freight?'
    a: 'Sea freight becomes cheaper than air around 200kg / 2 CBM. Below that, air or express usually wins on speed + cost.'
---

CBM and dimensional weight are the two numbers that decide what you pay for shipping. Get them wrong and you either overpay or get a surprise adjustment bill.

## What is CBM?

CBM = **cubic meter**. It's the volume of your shipment:

```
CBM = length (m) × width (m) × height (m)
```

Example: a box 60cm × 40cm × 30cm
```
0.6 × 0.4 × 0.3 = 0.072 CBM
```

For 10 identical boxes: 0.72 CBM.

## What is dimensional weight?

Dimensional weight (also "volumetric weight") accounts for the space a package takes up, not just its mass. Light but bulky items would be unfairly cheap if carriers only charged by actual weight.

```
Dimensional weight = (L × W × H in cm) ÷ divisor
```

The divisor depends on the carrier and mode:

| Mode | Divisor |
|---|---|
| Air freight | 6000 |
| Express (DHL, FedEx, UPS) | 5000 |
| Sea freight (LCL) | 1000 |
| USPS First-Class | 9000 |
| Amazon FBA inbound | 5000 |

## Carrier charges the higher number

For every shipment, the carrier calculates both:

- **Actual weight** (scale)
- **Dimensional weight** (volume ÷ divisor)

You pay for the **higher** of the two. This is called **chargeable weight**.

## Worked example

A box 50cm × 40cm × 30cm weighing 8kg, shipping via DHL:

```
Actual weight:        8 kg
Dimensional weight:   (50 × 40 × 30) ÷ 5000 = 60000 ÷ 5000 = 12 kg
Chargeable weight:    12 kg
```

You pay for 12kg, not 8kg. Even though the scale reads 8.

## When dimensional weight kicks in

Rule of thumb: if your product is **bulky and light** (pillows, foam, lampshades), dimensional weight always wins. If it's **dense and small** (books, metal parts), actual weight wins.

| Product type | Dimensional or actual? |
|---|---|
| Apparel (compressed) | Actual |
| Books | Actual |
| Foam, pillows, plush | Dimensional |
| Lampshades, baskets | Dimensional |
| Electronics (small) | Actual |
| Furniture parts | Dimensional |
| Supplements, cosmetics | Actual |
| Inflatable products | Always dimensional |

## How to reduce dimensional weight

You can't change the math, but you can change the packaging:

1. **Use the smallest box that fits** — every cm counts. Don't ship a 50cm box when a 40cm box works.
2. **Compress soft goods** — apparel under vacuum bags cuts dimensional weight by 30–50%.
3. **Break into multiple boxes** — two 5kg boxes often ship cheaper than one 10kg box with awkward dimensions.
4. **Flat-pack when possible** — folding items reduce volume dramatically.

## Worked example: packing optimization

10 shirts in a 50×40×30cm box, each shirt 200g:

```
Original box:
  Dimensions: 50 × 40 × 30 cm
  Actual weight: 2 kg
  Dimensional: 60000 ÷ 5000 = 12 kg
  Chargeable: 12 kg → shipping cost ~$66 (DHL)

Compressed + smaller box (40 × 30 × 20 cm):
  Actual weight: 2 kg
  Dimensional: 24000 ÷ 5000 = 4.8 kg
  Chargeable: 4.8 kg → shipping cost ~$26

Savings: 60%
```

## Sea freight LCL specifics

For Less-than-Container-Load (LCL) sea freight, the divisor is **1000** — meaning dimensional weight is much more punishing. A 1 CBM shipment of dense goods (1000kg actual) breaks even. Anything lighter pays for volume.

Most LCL carriers also have a **minimum 1 CBM charge**, even if your shipment is 0.3 CBM.

## Air freight vs express

| | Air freight | Express (DHL/FedEx) |
|---|---|---|
| Divisor | 6000 | 5000 |
| Price/kg | $4–8 | $6–12 |
| Best for | 100kg+ bulk | < 100kg urgent |
| Transit | 5–10 days | 3–7 days |
| Tracking | Basic | Real-time |

Express uses a smaller divisor (5000 vs 6000), so dimensional weight is higher — making express proportionally more expensive for bulky items.

## Quick reference: when each mode wins

| Shipment profile | Best mode |
|---|---|
| < 20kg, urgent | Express |
| 20–200kg, dense | Express or air |
| 100–500kg, any density | Air freight |
| 200kg+ / 2 CBM+, not urgent | Sea LCL |
| Full container (28+ CBM) | Sea FCL |

## Tools to use

- **[CBM calculator](/tools/)** — coming soon
- **[Product Pricing Calculator](/tools/pricing-calculator/)** — bake shipping cost into your pricing
- **Shipping cost spreadsheet** — see [resources](/resources/)