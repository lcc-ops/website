---
title: 'CBM & Dimensional Weight Calculator'
description: 'Compute CBM (m³), chargeable weight, total weight and boxes needed for air and sea freight quotes.'
pubDate: 2026-06-30
category: 'shipping'
tags: ['cbm', 'dimensional weight', 'shipping', 'air freight', 'sea freight', 'logistics']
icon: '📦'
component: 'CbmCalculator'
translationKey: 'cbm-calculator'
tldr: 'CBM = (L × W × H in cm) ÷ 1,000,000. Volumetric weight = (L × W × H) ÷ 6000 (air) or ÷ 10000 (sea). Chargeable weight is the greater of actual and volumetric weight.'
faq:
  - q: 'What is the difference between CBM and dimensional weight?'
    a: 'CBM measures physical volume (1 m³ = the space of a cube one meter on each side). Dimensional (volumetric) weight converts that volume into a weight equivalent, because carriers charge by whichever is larger: actual weight or the volume-based equivalent. Air freight uses a divisor of 6000; sea freight uses 10000.'
  - q: 'How is chargeable weight calculated?'
    a: 'Chargeable weight = max(actual weight, volumetric weight). Volumetric weight = (length × width × height in cm) ÷ divisor (6000 for air, 10000 for sea). Multiply by quantity for the total chargeable weight of the shipment.'
  - q: 'When should I use air vs sea for volumetric shipments?'
    a: 'Use air when your product is high-density, time-sensitive, or the order value per kg justifies express cost. Use sea when the volume-to-weight ratio is poor (e.g. foam, plastic containers) — sea''s 10000 divisor softens the volumetric penalty and lowers cost per shipment.'
  - q: 'What is the industry standard box dimension?'
    a: 'There is no universal box. Common FBA-ready cartons are 40×30×20 cm (24 L). LCL sea shipments often use 50×40×30 or 60×40×40. Match the inner dimensions to your product plus 1–2 cm of padding.'
  - q: 'Does Amazon FBA bill by dimensional weight?'
    a: 'No. Amazon FBA uses its own size tiers (small standard, large standard, etc.) based on unit weight and longest side, billed per unit. For 3PL or freight legs to Amazon''s warehouse, dimensional weight still applies.'
  - q: 'Can I save money by combining boxes?'
    a: 'Not always. One big box often pushes you into a higher dimensional-weight bracket. Split into multiple smaller cartons, leave headroom for weight distribution, and verify the carrier''s oversize surcharges before consolidating.'
---

CBM and dimensional weight are not the same. CBM is **physical volume** — how much three-dimensional space your shipment occupies in cubic meters. Dimensional (or volumetric) weight is a **pricing construct** that converts that volume into a weight equivalent so carriers can charge fairly for space when goods are large but light.

Carriers charge you based on the **greater** of actual weight or volumetric weight. That's why a pallet of foam pillows can weigh 50 kg yet bill as 300 kg — the volume takes more space than the mass suggests.

## How this calculator works

1. **Length, width, height (cm)** — single-unit carton dimensions.
2. **Weight per unit (kg)** — gross weight including packaging.
3. **Quantity** — how many cartons (or how many units if packed together).
4. **Mode** — air (divisor 6000) or sea (divisor 10000).

The tool returns:

- **Total CBM** = L × W × H × qty ÷ 1,000,000
- **Total weight** = weight × qty
- **Chargeable weight** = max(total weight, total volume ÷ divisor)

For mixed shipments, run the calculator once per SKU and sum the chargeable weights.

## Real shipment reference

| Product | Carton L×W×H (cm) | Weight (kg) | Qty | Mode | Total CBM | Chargeable | Per-unit cost impact |
|---|---|---|---|---|---|---|---|
| Phone case | 50 × 40 × 30 | 2.5 | 20 | Air | 0.12 | 20.0 kg (vol) | $0.30 / unit (air) |
| Cotton T-shirt | 60 × 40 × 40 | 12 | 50 | Air | 0.48 | 80.0 kg (vol) | $0.18 / unit |
| Pillow insert | 60 × 40 × 40 | 1.2 | 80 | Sea | 0.77 | 76.8 kg (vol) | $0.04 / unit (sea wins) |
| Bluetooth speaker | 45 × 35 × 25 | 8 | 30 | Air | 0.118 | 30.0 kg (actual) | $0.12 / unit |

Three of the four rows above are billed by **volumetric** weight, not actual weight — the cotton T-shirts look heavy (12 kg per carton) but volumetric 80 kg is what gets billed. The pillow insert example is the classic case where switching from air to sea halves the per-unit freight cost.

## Why the divisor matters

The divisor is the carrier's price lever. Smaller divisor → larger volumetric weight → higher bill. Air freight's 6000 divisor effectively says "1 m³ of air freight equals 167 kg of product." Sea's 10000 divisor relaxes that to 100 kg per m³.

If a forwarder quotes a different divisor (5000, 7000), ask **why**. Some markets (e.g. China domestic, certain Latam lanes) use non-standard divisors. The International Air Transport Association (IATA) standard is 6000.

## Common mistakes

- **Forgetting inner-pack density** — 50 phone cases packed into one 50×40×30 box with foam void fill changes the billable dimension but not the product weight.
- **Mixing modes inside one PO** — the calculator assumes all units share the same mode. Run the math separately for each leg.
- **Trusting supplier carton weights** — they often quote **net** weight. Add 8–15% for outer carton, pallet wrap, and dunnage.
- **Ignoring carrier minimums** — many express couriers have a 21 kg minimum even for a 2 kg parcel, billed at the minimum rate.

## Practical tips

- **Round up to the next 0.5 kg** — carriers bill by the heavier of decimals.
- **Always measure the outer carton**, not the product. Pallet wrap and void fill add 5–10%.
- **Group by destination and dim tier** if you ship multiple SKUs to optimize cartons per shipment.
- **Ask about minimum chargeable weight** — many carriers have a 21 kg or 25 kg minimum even for tiny parcels.
- **Quote with both divisors** — give your forwarder the air and sea numbers from this calculator, then negotiate from there.

## When this calculator is not enough

- **Multi-leg shipments** (factory → port → Amazon warehouse) need separate runs per leg with different divisors.
- **FBA inbound** uses Amazon's own size tiers, not dim weight. See [Amazon FBA fee math](#) for the tier table.
- **Hazardous or oversized cargo** triggers surcharge schedules beyond simple volumetric math.

## Workflow

1. Measure each SKU's outer carton after packing.
2. Run this calculator once per SKU, export the chargeable weight.
3. Cross-check against the forwarder's quote using both divisors.
4. Feed total freight into the [Pricing Calculator](/tools/pricing-calculator/) for landed-cost pricing.

## Tools & reading

- **[Product Pricing Calculator](/tools/pricing-calculator/)** — fold shipping cost into your landed price
- **[Fee Comparator](/tools/fee-comparator/)** — adjust margins for processor fees
- **Shipping math guide** — [CBM and dimensional weight explained](/content/cbm-and-dimensional-weight/)