export const SITE = {
  name: 'website',
  title: 'A Minimalist Hub for Tools & Writing',
  description:
    'A static-first, edge-fast personal site for practical tools and SEO-friendly writing.',
  author: 'lcc-ops',
  email: 'contact@example.com',
  social: {
    github: 'https://github.com/lcc-ops',
  },
  analytics: {
    // Cloudflare Web Analytics beacon — fill after deploying to Pages
    cfBeacon: '',
  },
  ads: {
    // Google AdSense slot — keep blank until AdSense is approved
    enabled: false,
    client: '',
  },
} as const;
