// scripts/check/link_check.mjs
//
// Site link checker — diagnostic tool, not a CI gate. Always exits 0.
//
// Head-fetches every URL the public sitemap emits (built from src/pages/
// the same way astro.config.mjs does at config time), plus the static
// routes derived from the live filesystem. Writes a tabular report to
// _out_linkcheck.txt so the run is auditable after the fact.
//
// Tunables:
//   SITE_URL    — base; defaults to the same value astro.config.mjs uses.
//                 Override for local dev (e.g. SITE_URL=http://127.0.0.1:4321).
//   SLOW_MS     — slow threshold (default 1500 ms)
//   TIMEOUT_MS  — fetch timeout (default 5000 ms)
//   OUT_PATH    — override the output path (default ../scripts/check/_out_linkcheck.txt
//                 relative to this script — i.e. this very directory)

import { readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import { performance } from 'node:perf_hooks';

const SITE_URL = process.env.SITE_URL ?? 'https://kuajinglab.xyz';
const SLOW_MS = Number(process.env.SLOW_MS ?? 1500);
const TIMEOUT_MS = Number(process.env.TIMEOUT_MS ?? 5000);
const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..', '..');
const OUT_PATH =
  process.env.OUT_PATH ??
  join(__dirname, '_out_linkcheck.txt');

// Mirrors astro.config.mjs:18-31 — collect content/tools slugs from disk so
// the link check reflects *current* content (post-draft) without re-running
// config.
const collectSlugs = (base) => {
  const out = new Set();
  try {
    for (const entry of readdirSync(base, { withFileTypes: true })) {
      if (entry.isDirectory()) out.add(entry.name);
    }
  } catch {
    // Base directory may be missing on a fresh checkout.
  }
  return out;
};

const blogSlugs = [...collectSlugs(join(REPO_ROOT, 'src', 'content', 'blog'))];
const toolSlugs = [...collectSlugs(join(REPO_ROOT, 'src', 'content', 'tools'))];

// Static routes — top-level .astro files plus their /zh/ twin when present.
// Derived from `find src/pages -maxdepth 1 -name '*.astro'`. /blog and
// /zh/blog are skipped because astro.config.mjs:97-103 redirects them to
// /content and /zh/content respectively; hitting /blog/ would always be 301.
const PAGES_DIR = join(REPO_ROOT, 'src', 'pages');
const ZH_PAGES_DIR = join(PAGES_DIR, 'zh');
const topLevelAstro = readdirSync(PAGES_DIR, { withFileTypes: true })
  .filter((d) => d.isFile() && d.name.endsWith('.astro'))
  .map((d) => d.name.replace(/\.astro$/, ''));
const zhSubdirAstro = (() => {
  try {
    return readdirSync(ZH_PAGES_DIR, { withFileTypes: true })
      .filter((d) => d.isFile() && d.name.endsWith('.astro'))
      .map((d) => d.name.replace(/\.astro$/, ''));
  } catch {
    return [];
  }
})();

const enOnlyRoutes = topLevelAstro
  .filter((p) => !zhSubdirAstro.includes(p))
  .map((p) => `/${p}/`);
const zhOnlyRoutes = zhSubdirAstro.map((p) => `/${p}/`);
const bilingualRoutes = topLevelAstro
  .filter((p) => zhSubdirAstro.includes(p) && p !== 'index')
  .flatMap((p) => [`/${p}/`, `/${p === 'index' ? '' : 'zh/'}${p === 'index' ? '' : p}/`]);

const STATIC_ROUTES = [
  ...enOnlyRoutes,
  ...zhOnlyRoutes,
  ...bilingualRoutes,
].filter((u, i, arr) => arr.indexOf(u) === i);

const DYNAMIC_ROUTES = [
  ...blogSlugs.flatMap((s) => [`/content/${s}/`, `/zh/content/${s}/`]),
  ...toolSlugs.flatMap((s) => [`/tools/${s}/`, `/zh/tools/${s}/`]),
];

const ALL_PATHS = [...new Set([...STATIC_ROUTES, ...DYNAMIC_ROUTES])]
  .sort((a, b) => a.localeCompare(b));
const ALL_URLS = ALL_PATHS.map((p) => `${SITE_URL.replace(/\/$/, '')}${p}`);

let ok = 0, slow = 0, fail = 0, err = 0;

const head = async (url) => {
  const start = performance.now();
  try {
    const res = await fetch(url, {
      method: 'HEAD',
      signal: AbortSignal.timeout(TIMEOUT_MS),
      redirect: 'follow',
    });
    const ms = performance.now() - start;
    const status = res.status;
    if (status >= 400) { fail += 1; return { url, status, ms, kind: 'FAIL' }; }
    if (ms > SLOW_MS) { slow += 1; return { url, status, ms, kind: 'SLOW' }; }
    ok += 1;
    return { url, status, ms, kind: 'OK' };
  } catch (e) {
    err += 1;
    return {
      url,
      status: 'ERR',
      ms: performance.now() - start,
      kind: 'FAIL',
      err: e instanceof Error ? e.message : String(e),
    };
  }
};

const stamp = new Date().toISOString();
const lines = [];
lines.push(`=== link_check ${stamp} ===`);
lines.push(`site:    ${SITE_URL}`);
lines.push(`static:  ${STATIC_ROUTES.length}`);
lines.push(`dynamic: ${DYNAMIC_ROUTES.length} (blog=${blogSlugs.length}, tools=${toolSlugs.length})`);
lines.push(`total:   ${ALL_URLS.length}`);
lines.push(`slow:    > ${SLOW_MS} ms`);
lines.push(`timeout: ${TIMEOUT_MS} ms`);
lines.push('');

// Sequential HEAD — public site worker would coalesce, but keep it linear
// to avoid surprise when running against the live domain.
for (const url of ALL_URLS) {
  const r = await head(url);
  if (r.kind === 'FAIL') {
    lines.push(`[${r.ms.toFixed(0)} ms] ${r.status} ${r.url}${r.err ? '  (' + r.err + ')' : ''}  WARN`);
  } else if (r.kind === 'SLOW') {
    lines.push(`[${r.ms.toFixed(0)} ms] ${r.status} ${r.url}  WARN`);
  } else {
    lines.push(`[${r.ms.toFixed(0)} ms] ${r.status} ${r.url}`);
  }
}

lines.push('');
lines.push(`=== OK ${ok} / SLOW ${slow} / FAIL ${fail} / NETERR ${err} / TOTAL ${ALL_URLS.length} ===`);

const report = lines.join('\n') + '\n';

writeFileSync(OUT_PATH, report, 'utf8');

// eslint-disable-next-line no-console
console.log(report);

// Diagnostic tool — never fail the build. Caller can grep FAIL/NETERR.
process.exit(0);
