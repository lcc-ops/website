export const languages = {
  en: 'English',
  zh: '简体中文',
} as const;

export type Locale = keyof typeof languages;

export const defaultLocale: Locale = 'en';

type UIDict = Record<string, string>;

const en: UIDict = {
  'nav.home': 'Home',
  'nav.blog': 'Blog',
  'nav.tools': 'Tools',
  'nav.about': 'About',
  'nav.search': 'Search',
  'nav.theme': 'Toggle theme',
  'site.title': 'A Minimalist Hub for Tools & Writing',
  'site.tagline': 'Static-first, edge-fast, content-driven.',
  'footer.copyright': 'All rights reserved.',
  'footer.privacy': 'Privacy',
  'footer.terms': 'Terms',
  'blog.readMore': 'Read more',
  'blog.minutes': 'min read',
  'blog.publishedOn': 'Published on',
  'blog.category': 'Category',
  'blog.tag': 'Tags',
  'blog.archive': 'Archive',
  'blog.relatedTools': 'Related tools',
  'blog.relatedPosts': 'Related reading',
  'tools.title': 'Tools',
  'tools.subtitle': 'Lightweight utilities that run entirely in your browser.',
  'tools.openTool': 'Open tool',
  'ad.disclosure': 'Advertisement',
  'common.toc': 'On this page',
  'common.faq': 'Frequently asked questions',
  'common.copy': 'Copy',
  'common.copied': 'Copied',
};

const zh: UIDict = {
  'nav.home': '首页',
  'nav.blog': '博客',
  'nav.tools': '工具',
  'nav.about': '关于',
  'nav.search': '搜索',
  'nav.theme': '切换主题',
  'site.title': '极简工具与写作小站',
  'site.tagline': '静态优先，边缘加速，内容驱动。',
  'footer.copyright': '保留所有权利。',
  'footer.privacy': '隐私政策',
  'footer.terms': '服务条款',
  'blog.readMore': '继续阅读',
  'blog.minutes': '分钟阅读',
  'blog.publishedOn': '发布于',
  'blog.category': '分类',
  'blog.tag': '标签',
  'blog.archive': '归档',
  'blog.relatedTools': '相关工具',
  'blog.relatedPosts': '相关文章',
  'tools.title': '工具',
  'tools.subtitle': '完全在浏览器中运行的轻量工具。',
  'tools.openTool': '打开工具',
  'ad.disclosure': '广告',
  'common.toc': '本页目录',
  'common.faq': '常见问题',
  'common.copy': '复制',
  'common.copied': '已复制',
};

export const ui: Record<Locale, UIDict> = { en, zh };

export type UIKey = keyof (typeof ui)[Locale];

export function t(locale: Locale, key: string): string {
  return ui[locale]?.[key] ?? ui[defaultLocale]?.[key] ?? key;
}
