export const SITE = {
  name: 'Crossborder Cost Lab',
  title: 'Crossborder Cost Lab — Pricing, Shipping & Ad Math for Cross-border Sellers',
  description:
    'Pricing formulas, shipping math, payment fees and ad ROI for cross-border sellers. Free calculators, no signup.',
  shortName: 'CCL',
  author: 'lcc-ops',
  email: 'contact@kuajinglab.xyz',
  social: {
    github: 'https://github.com/lcc-ops/website',
  },
  analytics: {
    // Cloudflare Web Analytics beacon — fill after deploying to Workers
    cfBeacon: '',
  },
  ads: {
    // Google AdSense slot — keep blank until AdSense is approved
    enabled: false,
    client: '',
  },
  // Source of truth for the FX calculator's currency dropdown. Both
  // FxWithdrawCalculator and the home-page stats read from this list.
  // Update here, not in the .astro file.
  fxCurrencies: ['USD', 'EUR', 'GBP', 'JPY', 'CNY'],
} as const;