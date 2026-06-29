import type { GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';
import { renderOgCard } from '~/lib/og';
import { categoryLabels, type Locale } from '~/i18n/ui';

export const prerender = true;

export const getStaticPaths: GetStaticPaths = async () => {
  const tools = await getCollection('tools');
  return tools
    .filter((t) => t.id.endsWith('/en') || t.id.endsWith('/zh'))
    .map((t) => {
      const lang = t.id.endsWith('/en') ? 'en' : 'zh';
      const slug = t.id.split('/')[0];
      return { params: { slug, lang }, props: { tool: t, lang: lang as Locale } };
    });
};

export const GET = async ({
  props,
}: {
  props: { tool: Awaited<ReturnType<typeof getCollection<'tools'>>>[number]; lang: Locale };
}) => {
  const { tool, lang } = props;
  const subtitle = `${categoryLabels[lang][tool.data.category] ?? tool.data.category} · Calculator`;
  const brand = 'Crossborder Cost Lab';
  const svg = renderOgCard({ subtitle, title: tool.data.title, brand });
  return new Response(svg, {
    status: 200,
    headers: {
      'Content-Type': 'image/svg+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
