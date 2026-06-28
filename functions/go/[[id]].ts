/**
 * /go/:id — outbound redirector with click tracking via Cloudflare Analytics Engine.
 *
 * Mapping rules live in the LINK_MAP constant; update as you add affiliate links.
 * Falls through to 404 if the id is unknown — no open redirect.
 */
export interface Env {
  // Bind when you want to persist stats:  npx wrangler kv:namespace create GO_STATS
  // and add the binding to wrangler.toml / Pages dashboard.
  GO_STATS?: KVNamespace;
}

const LINK_MAP: Record<string, { url: string; label?: string }> = {
  sample: { url: 'https://example.com/sample-resource', label: 'Sample' },
  // Add more as you onboard programs. Never let an external ?url= parameter pass through.
};

export const onRequest: PagesFunction<Env> = async (context) => {
  const { params, env } = context;
  const id = (params.id as string | undefined) ?? '';
  const target = LINK_MAP[id];

  if (!target) {
    return new Response('Not found', { status: 404 });
  }

  // Lightweight, no-cookie counter via KV if bound; else just log.
  if (env.GO_STATS) {
    const today = new Date().toISOString().slice(0, 10);
    const key = `go:${id}:${today}`;
    context.waitUntil(env.GO_STATS.put(key, String(Number((await env.GO_STATS.get(key)) ?? '0') + 1)));
  }

  return Response.redirect(target.url, 302);
};
