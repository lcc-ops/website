// @ts-check
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

import rehypeSlug from 'rehype-slug';
import rehypeExternalLinks from 'rehype-external-links';
import remarkGfm from 'remark-gfm';
import { readdirSync } from 'node:fs';

const SITE_URL = 'https://kuajinglab.xyz';

// Collect every entry folder under a content collection base. Each folder
// represents one slug and must contain both en.md and zh.md (verified by
// convention in src/content.config.ts). Returning a Set dedupes accidental
// collisions.
const collectSlugs = (/** @type {string} */ base) => {
  /** @type {Set<string>} */
  const out = new Set();
  try {
    for (const entry of /** @type {import('node:fs').Dirent[]} */ (
      readdirSync(base, { withFileTypes: true })
    )) {
      if (entry.isDirectory()) out.add(entry.name);
    }
  } catch {
    // Base directory may be missing on a fresh checkout — ignore.
  }
  return out;
};

// @astrojs/sitemap does not enumerate dynamic routes in SSR mode. Inject
// every content + tools slug in both locales so search engines can find them.
const contentSlugs = [...collectSlugs('./src/content/blog')];
const toolSlugs = [...collectSlugs('./src/content/tools')];

const localizedContentPages = contentSlugs.flatMap((slug) => [
  `${SITE_URL}/content/${slug}/`,
  `${SITE_URL}/zh/content/${slug}/`,
]);
const localizedToolPages = toolSlugs.flatMap((slug) => [
  `${SITE_URL}/tools/${slug}/`,
  `${SITE_URL}/zh/tools/${slug}/`,
]);

const customPages = [...localizedContentPages, ...localizedToolPages];

export default defineConfig({
  site: 'https://kuajinglab.xyz',
  output: 'server',
  adapter: cloudflare({
    imageService: 'cloudflare',
  }),
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  prefetch: {
    prefetchAll: true,
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark-dimmed',
      wrap: true,
    },
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [
        rehypeExternalLinks,
        { target: '_blank', rel: ['noopener', 'noreferrer'] },
      ],
    ],
  },
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    sitemap({
      customPages,
      i18n: {
        defaultLocale: 'en',
        locales: {
          en: 'en-US',
          zh: 'zh-CN',
        },
      },
    }),
  ],
  // Redirect legacy /blog URLs to /content. Old URLs were shaped
  // /blog/<slug>/<lang> and /zh/blog/<slug>/<lang>; the new layout puts the
  // locale in the URL prefix only, so we drop the trailing <lang> segment.
  redirects: {
    '/blog': '/content',
    '/zh/blog': '/zh/content',
    '/blog/[slug]/[lang]': '/content/[slug]',
    '/zh/blog/[slug]/[lang]': '/zh/content/[slug]',
    '/zh/rss.xml': '/rss.xml',
  },
});
