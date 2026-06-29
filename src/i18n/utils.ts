import { defaultLocale, type Locale, languages } from './ui.ts';

export const SITE_URL = 'https://website.2088643687.workers.dev';

export function getLocaleFromUrl(url: URL): Locale {
  const [, seg] = url.pathname.split('/');
  if (seg && seg in languages) return seg as Locale;
  return defaultLocale;
}

export function localizePath(path: string, locale: Locale): string {
  const cleaned = path.startsWith('/') ? path : `/${path}`;
  if (locale === defaultLocale) return cleaned;
  return `/${locale}${cleaned === '/' ? '' : cleaned}`;
}

export function dateFormatter(locale: Locale): Intl.DateTimeFormat {
  const map: Record<Locale, string> = { en: 'en-US', zh: 'zh-CN' };
  return new Intl.DateTimeFormat(map[locale], {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}
