export const languages = {
  en: 'English',
  zh: '简体中文',
} as const;

export type Locale = keyof typeof languages;

export const defaultLocale: Locale = 'en';

type UIDict = Record<string, string>;

const en: UIDict = {
  // Navigation
  'nav.home': 'Home',
  'nav.content': 'Content',
  'nav.tools': 'Calculators',
  'nav.resources': 'Resources',
  'nav.about': 'About',
  'nav.search': 'Search',
  'nav.theme': 'Toggle theme',
  // Site identity
  'site.title': 'Crossborder Cost Lab',
  'site.tagline': 'Free calculators and practical guides to price, ship and profit on every cross-border order.',
  'site.description': 'Pricing formulas, shipping math, payment fees and ad ROI for cross-border sellers. Free calculators, no signup.',
  // Footer
  'footer.copyright': 'All rights reserved.',
  'footer.privacy': 'Privacy',
  'footer.terms': 'Terms',
  // Content categories (nav chips + section labels)
  'category.pricing': 'Pricing',
  'category.shipping': 'Shipping',
  'category.payment': 'Payment',
  'category.ads': 'Ads',
  'category.ops': 'Ops',
  'category.cbm': 'Dimensional weight',
  'category.tool': 'Tool review',
  'category.guide': 'Beginner',
  // Hero / home
  'home.hero.eyebrow': 'Cross-border seller math',
  'home.hero.title': 'Price it right, ship it smart, profit on every order.',
  'home.hero.subtitle': 'Five free calculators and a growing library of practical guides. Built for Shopify, WooCommerce and Dropshipping sellers who want to stop guessing.',
  'home.hero.cta.calculators': 'Open calculators',
  'home.hero.cta.guides': 'Read the guides',
  'home.section.calculators': 'Calculators',
  'home.section.calculators.subtitle': 'Five tools that answer the questions every seller asks.',
  'home.section.categories': 'Browse by category',
  'home.section.guides': 'Latest guides',
  'home.section.guides.subtitle': 'In-depth walkthroughs with formulas, examples and downloads.',
  // Blog / content UI
  'blog.readMore': 'Read more',
  'blog.minutes': 'min read',
  'blog.publishedOn': 'Published on',
  'blog.updatedOn': 'Updated on',
  'blog.category': 'Category',
  'blog.tag': 'Tags',
  'blog.archive': 'Archive',
  'blog.relatedTools': 'Related calculators',
  'blog.relatedPosts': 'Related reading',
  'blog.allInCategory': 'All in {category}',
  'blog.noPosts': 'No posts yet — check back soon.',
  // Tools UI
  'tools.title': 'Calculators',
  'tools.subtitle': 'Five free calculators. Everything runs in your browser — your numbers never leave the page.',
  'tools.openTool': 'Open calculator',
  'tools.allCategories': 'All',
  // Ad
  'ad.disclosure': 'Advertisement',
  // Common
  'common.toc': 'On this page',
  'common.faq': 'Frequently asked questions',
  'common.copy': 'Copy',
  'common.copied': 'Copied',
  'common.share': 'Share',
  'common.download': 'Download',
  'common.calculator': 'Calculator',
  // Resources page
  'resources.title': 'Free resources',
  'resources.subtitle': 'Spreadsheet templates, SOP checklists and curated links. No email required.',
  'resources.disclosure': 'Some links are affiliate links. We may earn a small commission if you sign up.',
  // Tool-specific labels (used in components)
  'tool.cost': 'Cost',
  'tool.shipping': 'Shipping',
  'tool.fee': 'Fee',
  'tool.commission': 'Commission',
  'tool.payment': 'Payment',
  'tool.profit': 'Profit',
  'tool.margin': 'Margin',
  'tool.price': 'Price',
  'tool.result': 'Result',
  'tool.reset': 'Reset',
  'tool.fixedFee': 'Fixed fee',
  'tool.suggested': 'Suggested price',
  'tool.breakeven': 'Break-even price',
  'tool.perUnit': 'Profit per unit',
  // CBM calculator
  'tool.length': 'Length',
  'tool.width': 'Width',
  'tool.height': 'Height',
  'tool.weight': 'Weight',
  'tool.qty': 'Quantity',
  'tool.mode': 'Mode',
  'tool.mode.air': 'Air (÷6000)',
  'tool.mode.sea': 'Sea (÷10000)',
  'tool.cbm': 'CBM',
  'tool.chargeableWeight': 'Chargeable weight',
  'tool.totalCbm': 'Total CBM',
  'tool.totalWeight': 'Total weight',
  'tool.boxesNeeded': 'Boxes needed',
  // Fee comparator
  'tool.unitPrice': 'Unit price',
  'tool.monthlyVolume': 'Monthly orders',
  'tool.paypal': 'PayPal',
  'tool.stripe': 'Stripe',
  'tool.monthlyRevenue': 'Monthly revenue',
  'tool.monthlyFee': 'Monthly fee',
  'tool.effectiveFee': 'Effective fee rate',
  'tool.winner': 'Lower cost',
  // ROAS
  'tool.cogs': 'COGS + shipping',
  'tool.adSpend': 'Ad spend budget',
  'tool.targetMargin': 'Target margin',
  'tool.targetRoas': 'Target ROAS',
  'tool.breakEvenRoas': 'Break-even ROAS',
  'tool.maxCpa': 'Max CPA',
  'tool.maxCpc': 'Max CPC (CTR 1%)',
  // FX
  'tool.amount': 'Amount',
  'tool.fromCurrency': 'From',
  'tool.toCurrency': 'To',
  'tool.provider': 'Provider',
  'tool.receiveAmount': 'You receive',
  'tool.fxMargin': 'FX margin',
  'tool.withdrawFee': 'Withdraw fee',
};

const zh: UIDict = {
  // Navigation
  'nav.home': '首页',
  'nav.content': '内容',
  'nav.tools': '计算器',
  'nav.resources': '资源',
  'nav.about': '关于',
  'nav.search': '搜索',
  'nav.theme': '切换主题',
  // Site identity
  'site.title': '跨境成本实验室',
  'site.tagline': '免费计算器与实操指南，帮你算清每笔跨境订单的利润。',
  'site.description': '面向独立站、Dropshipping 和跨境卖家的定价公式、物流算账、收款费率与广告 ROI 工具。免费、无需注册。',
  // Footer
  'footer.copyright': '保留所有权利。',
  'footer.privacy': '隐私政策',
  'footer.terms': '服务条款',
  // Content categories
  'category.pricing': '定价',
  'category.shipping': '物流',
  'category.payment': '收款',
  'category.ads': '广告',
  'category.ops': '运营',
  'category.cbm': '体积重',
  'category.tool': '工具评测',
  'category.guide': '入门科普',
  // Hero / home
  'home.hero.eyebrow': '跨境卖家算账',
  'home.hero.title': '算对账、控住成本、每单都赚钱。',
  'home.hero.subtitle': '五款免费计算器 + 持续更新的实操指南。专为 Shopify、WooCommerce、Dropshipping 卖家打造。',
  'home.hero.cta.calculators': '打开计算器',
  'home.hero.cta.guides': '看实操指南',
  'home.section.calculators': '计算器',
  'home.section.calculators.subtitle': '五个工具，覆盖卖家每天都在问的问题。',
  'home.section.categories': '按品类浏览',
  'home.section.guides': '最新文章',
  'home.section.guides.subtitle': '深度教程，含公式、案例与配套资源。',
  // Blog / content UI
  'blog.readMore': '继续阅读',
  'blog.minutes': '分钟阅读',
  'blog.publishedOn': '发布于',
  'blog.updatedOn': '更新于',
  'blog.category': '分类',
  'blog.tag': '标签',
  'blog.archive': '归档',
  'blog.relatedTools': '相关计算器',
  'blog.relatedPosts': '相关文章',
  'blog.allInCategory': '查看「{category}」全部',
  'blog.noPosts': '暂无文章，敬请期待。',
  // Tools UI
  'tools.title': '计算器',
  'tools.subtitle': '五款免费计算器，全部在浏览器内运行 — 你的数据不会离开页面。',
  'tools.openTool': '打开计算器',
  'tools.allCategories': '全部',
  // Ad
  'ad.disclosure': '广告',
  // Common
  'common.toc': '本页目录',
  'common.faq': '常见问题',
  'common.copy': '复制',
  'common.copied': '已复制',
  'common.share': '分享',
  'common.download': '下载',
  'common.calculator': '计算器',
  // Resources page
  'resources.title': '免费资源',
  'resources.subtitle': 'Excel 模板、SOP 检查清单与精选工具合集。无需邮箱。',
  'resources.disclosure': '部分链接为联盟推广链接，签约可能获得佣金。',
  // Tool-specific labels
  'tool.cost': '成本',
  'tool.shipping': '物流',
  'tool.fee': '手续费',
  'tool.commission': '佣金',
  'tool.payment': '收款',
  'tool.profit': '利润',
  'tool.margin': '利润率',
  'tool.price': '售价',
  'tool.result': '结果',
  'tool.reset': '重置',
  'tool.fixedFee': '固定费',
  'tool.suggested': '建议售价',
  'tool.breakeven': '盈亏平衡价',
  'tool.perUnit': '单件利润',
  // CBM 计算器
  'tool.length': '长',
  'tool.width': '宽',
  'tool.height': '高',
  'tool.weight': '重量',
  'tool.qty': '数量',
  'tool.mode': '模式',
  'tool.mode.air': '空运 (÷6000)',
  'tool.mode.sea': '海运 (÷10000)',
  'tool.cbm': '体积',
  'tool.chargeableWeight': '计费重',
  'tool.totalCbm': '总体积',
  'tool.totalWeight': '总重量',
  'tool.boxesNeeded': '所需箱数',
  // 费率对比
  'tool.unitPrice': '客单价',
  'tool.monthlyVolume': '月单量',
  'tool.paypal': 'PayPal',
  'tool.stripe': 'Stripe',
  'tool.monthlyRevenue': '月流水',
  'tool.monthlyFee': '月手续费',
  'tool.effectiveFee': '有效费率',
  'tool.winner': '更低',
  // ROAS
  'tool.cogs': '成本 + 物流',
  'tool.adSpend': '广告预算',
  'tool.targetMargin': '目标利润率',
  'tool.targetRoas': '目标 ROAS',
  'tool.breakEvenRoas': '保本 ROAS',
  'tool.maxCpa': '最高 CPA',
  'tool.maxCpc': '最高 CPC (CTR 1%)',
  // 汇率提现
  'tool.amount': '金额',
  'tool.fromCurrency': '原币',
  'tool.toCurrency': '目标',
  'tool.provider': '服务商',
  'tool.receiveAmount': '到账金额',
  'tool.fxMargin': '汇率点差',
  'tool.withdrawFee': '提现手续费',
};

export const ui: Record<Locale, UIDict> = { en, zh };

export type UIKey = keyof (typeof ui)[Locale];

export function t(locale: Locale, key: string, params?: Record<string, string | number>): string {
  let value = ui[locale]?.[key] ?? ui[defaultLocale]?.[key] ?? key;
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      value = value.replaceAll(`{${k}}`, String(v));
    }
  }
  return value;
}

export const categoryLabels: Record<Locale, Record<string, string>> = {
  en: {
    pricing: 'Pricing',
    shipping: 'Shipping',
    payment: 'Payment',
    ads: 'Ads',
    ops: 'Ops',
    cbm: 'Dimensional weight',
    tool: 'Tool review',
    guide: 'Beginner',
  },
  zh: {
    pricing: '定价',
    shipping: '物流',
    payment: '收款',
    ads: '广告',
    ops: '运营',
    cbm: '体积重',
    tool: '工具评测',
    guide: '入门科普',
  },
};