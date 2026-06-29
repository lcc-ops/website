import type { GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';
import { renderOgCard } from '~/lib/og';
import { categoryLabels, type Locale } from '~/i18n/ui';

export const prerender = true;

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await getCollection('content', ({ data }) => !data.draft);
  return posts
    .filter((p) => p.id.endsWith('/en') || p.id.endsWith('/zh'))
    .map((p) => {
      const lang = p.id.endsWith('/en') ? 'en' : 'zh';
      const slug = p.id.split('/')[0];
      return { params: { slug, lang }, props: { post: p, lang: lang as Locale } };
    });
};

export const GET = async ({
  props,
}: {
  props: { post: Awaited<ReturnType<typeof getCollection<'content'>>>[number]; lang: Locale };
}) => {
  const { post, lang } = props;
  const subtitle = categoryLabels[lang][post.data.category] ?? post.data.category;
  const brand = 'Crossborder Cost Lab';
  const svg = renderOgCard({ subtitle, title: post.data.title, brand });
  return new Response(svg, {
    status: 200,
    headers: {
      'Content-Type': 'image/svg+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
