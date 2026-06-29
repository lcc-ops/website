// @ts-check
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

import rehypeSlug from 'rehype-slug';
import rehypeExternalLinks from 'rehype-external-links';
import remarkGfm from 'remark-gfm';

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
