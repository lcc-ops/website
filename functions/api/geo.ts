/**
 * /api/geo — returns a minimal locale hint from Cloudflare's cf-ipcountry header
 * so the client can pre-select a language without a full IP database.
 *
 * The page already stores preference in localStorage; this endpoint is just a hint
 * for first-visit visitors. No PII is collected.
 */
export const onRequestGet: PagesFunction = async ({ request }) => {
  const country = request.headers.get('cf-ipcountry') ?? 'XX';
  const locale = country === 'CN' || country === 'TW' || country === 'HK' || country === 'SG'
    ? 'zh'
    : 'en';
  return new Response(JSON.stringify({ locale, country }), {
    headers: {
      'content-type': 'application/json',
      'cache-control': 'public, max-age=86400',
    },
  });
};
