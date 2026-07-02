import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '~/site.config';
import { defaultLocale } from '~/i18n/ui';

export async function GET(context: APIContext) {
  const posts = (await getCollection('content', ({ data }) => !data.draft))
    .filter((p) => p.id.endsWith(`/${defaultLocale}`))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  // Source repo URL is intentionally not exposed; use the published site.
  const site = context.site ?? new URL('https://kuajinglab.xyz');

  return rss({
    title: SITE.title,
    description: SITE.description,
    site,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/content/${post.id.split('/')[0]}`,
      categories: [post.data.category, ...post.data.tags],
    })),
    customData: `<language>${defaultLocale}-${defaultLocale === 'zh' ? 'CN' : 'US'}</language>`,
  });
}
