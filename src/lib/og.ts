/**
 * OG image SVG renderer.
 *
 * Produces a 1200x630 SVG card (Twitter / OG spec) with:
 *   - subtitle (small, top-left)
 *   - title (large, center)
 *   - brand mark (bottom-right)
 *
 * Pure string assembly — no DOM, no runtime deps. Safe to call from
 * SSR endpoints; output is XML-safe.
 */

export interface OgCardInput {
  /** Small eyebrow text above the title (e.g. "Pricing guide"). */
  subtitle: string;
  /** Main title (e.g. article / tool name). Up to ~80 chars; we truncate. */
  title: string;
  /** Brand mark shown in the bottom-right corner. */
  brand: string;
  /** Optional accent line color override. */
  accent?: string;
}

const WIDTH = 1200;
const HEIGHT = 630;

const PALETTE = {
  bg: '#0b0b12',
  bgSoft: '#15151f',
  fg: '#f4f4f6',
  fgSoft: '#a0a0b0',
  accent: '#7c8cff',
} as const;

/** Escape a string for safe inclusion in XML text. */
function xmlEscape(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/** Soft-wrap a title into multiple <tspan> lines by character count. */
function wrapTitle(title: string, maxCharsPerLine: number, maxLines: number): string[] {
  const words = title.split(/\s+/);
  const lines: string[] = [];
  let current = '';
  for (const word of words) {
    const candidate = current ? `${current} ${word}` : word;
    if (candidate.length > maxCharsPerLine && current) {
      lines.push(current);
      current = word;
    } else {
      current = candidate;
    }
  }
  if (current) lines.push(current);
  // If still too many lines, hard-truncate the last visible line.
  if (lines.length > maxLines) {
    const kept = lines.slice(0, maxLines);
    const last = kept[maxLines - 1];
    kept[maxLines - 1] = last.length > maxCharsPerLine - 1
      ? `${last.slice(0, maxCharsPerLine - 1)}…`
      : `${last}…`;
    return kept;
  }
  return lines;
}

export function renderOgCard(input: OgCardInput): string {
  const accent = input.accent ?? PALETTE.accent;
  const titleLines = wrapTitle(input.title, 22, 3);

  const titleTspans = titleLines
    .map((line, i) =>
      `      <tspan x="80" dy="${i === 0 ? 0 : 88}">${xmlEscape(line)}</tspan>`,
    )
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="${xmlEscape(input.title)}">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${PALETTE.bg}"/>
      <stop offset="100%" stop-color="${PALETTE.bgSoft}"/>
    </linearGradient>
  </defs>
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="6" height="${HEIGHT}" fill="${accent}"/>

  <text x="80" y="120" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif" font-size="28" font-weight="500" fill="${PALETTE.fgSoft}" letter-spacing="2">
    ${xmlEscape(input.subtitle.toUpperCase())}
  </text>

  <text x="80" y="200" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif" font-size="76" font-weight="700" fill="${PALETTE.fg}">
${titleTspans}
  </text>

  <text x="${WIDTH - 80}" y="${HEIGHT - 60}" text-anchor="end" font-family="ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif" font-size="28" font-weight="600" fill="${accent}">
    ${xmlEscape(input.brand)}
  </text>
</svg>
`;
}
