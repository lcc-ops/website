// Shared copy for the About page (en + zh). Sourced in one place so the
// two locales do not drift. The English About used to live entirely inside
// src/pages/about.astro as a locale map; this module lifts it out so
// src/pages/zh/about.astro can render the same eight sections without a
// parallel hardcoded copy.

import type { Locale } from './ui';

export type AboutBoardItem = { role: string; who: string; note: string };

export type AboutCopy = {
  title: string;
  intro: string;
  who: string;
  forSellers: string;
  sideProject: string;
  principles: string[];
  contact: string;
  editorialTitle: string;
  editorialIntro: string;
  sourcingTitle: string;
  sourcingItems: string[];
  correctionsTitle: string;
  correctionsBody: string;
  reviewCadence: string;
  reviewBody: string;
  boardTitle: string;
  boardIntro: string;
  boardItems: AboutBoardItem[];
  transparencyTitle: string;
  transparencyBody: string;
  fundingTitle: string;
  fundingBody: string;
  partnerLinksTitle: string;
  partnerLinksBody: string;
  verifiedIdentitiesLabel: string;
  verifiedIdentitiesValue: string;
  knowsAbout: string[];
  personDescription: string;
};

export const aboutCopy: Record<Locale, AboutCopy> = {
  en: {
    title: 'About',
    intro:
      'A free toolkit that does the math so cross-border sellers can stop guessing and start pricing for profit.',
    who: "I run a small catalog of e-commerce stores selling from China to North America and Europe. The margins on cross-border orders are thin, and most of the loss hides inside numbers — payment fees, FX spreads, dimensional weight, ad waste — that nobody hands you a clean spreadsheet for. Crossborder Cost Lab is where I publish the calculators I built for my own shelves, so you don't have to rebuild them.",
    forSellers:
      'If you sell on Shopify, WooCommerce, Amazon, TikTok Shop or run a one-product dropshipping store, this site is for you. The tools assume you know your cost of goods, you already ship orders internationally, and you want answers in 30 seconds, not a 40-page whitepaper.',
    sideProject:
      'Side project: the AI Lab tracks independent AI products — revenue, business model, content flywheel, failure modes. Each case is sourced from public posts or filings and summarized with first-party analysis. The underlying math (margins, payback, lifetime value) is the same math used in the cross-border calculators.',
    principles: [
      'No login. No email gate. Every calculator works the moment the page loads.',
      'No black-box formulas. The math is visible, the assumptions are documented.',
      'No sponsored rankings. Tools are listed by what they answer, not what pays the most.',
    ],
    contact:
      'Spotted a wrong rate, a missing currency, or a calculation that breaks in the corner cases? Send a note to contact@kuajinglab.xyz — I read every one.',

    editorialTitle: 'Editorial standards',
    editorialIntro:
      'Everything published on this site is held to four rules. They are short on purpose — the point is that they are checkable.',
    sourcingTitle: 'How content is sourced and produced',
    sourcingItems: [
      'Tools are written from first-party formulas. Each one cites the underlying rate sheet (Stripe pricing page, PayPal fee table, Amazon FBA calculator output, carrier dimensional-weight tables) at the bottom of the page.',
      'AI Lab case studies are paraphrased summaries of public posts, interviews, or filings the operator has read. Every post links back to the original source on first mention; if no specific URL can be re-verified, the post carries an explicit "Source" disclosure block stating the post is a summary of publicly available material read by the operator.',
      'Numbers in tables (RPM, ARR, fee percentages) are quoted as the source states them. When a number is rounded, we say so. When it is disputed, we say who disputes it.',
      'No ghostwriting-for-hire, no auto-generated articles published without an editor pass, no auto-translation published without a native-reader review.',
    ],
    correctionsTitle: 'Corrections policy',
    correctionsBody:
      'If a tool produces a wrong number, or a post quotes a number that has since changed, we fix it within 7 days of being told. The fix is silent on the live page (date in the frontmatter is updated). For factual errors in posts, we add a dated correction note at the bottom of the page so the audit trail is visible.',
    reviewCadence: 'How often content is re-reviewed',
    reviewBody:
      'Every calculator is re-checked against its source rate sheet at least once per quarter. Posts that reference moving targets (carrier fees, ad CPM, AI product pricing) are re-checked at the same cadence and dated in the frontmatter. Pages we cannot re-verify against the original source are marked "stale" or removed.',
    boardTitle: 'Editorial responsibility',
    boardIntro:
      'Crossborder Cost Lab is run by one operator. For accountability the responsibilities below are split across named roles so it is clear who owns which class of decision.',
    boardItems: [
      { role: 'Publisher & lead editor', who: 'kuajinglab', note: 'Final say on what is published and what is retracted.' },
      { role: 'Source verification', who: 'kuajinglab', note: 'Re-checks each cited rate sheet quarterly; signs off before publication.' },
      { role: 'Math reviewer', who: 'kuajinglab', note: 'Walks each formula against an independent implementation before launch.' },
      { role: 'Corrections contact', who: 'kuajinglab', note: 'Reads every email to contact@kuajinglab.xyz and owns the corrections log.' },
    ],
    transparencyTitle: 'What this site is not',
    transparencyBody:
      'Crossborder Cost Lab is not a news outlet, not a financial advisor, not a tax preparer. Calculator outputs are estimates; cross-border fee structures change without notice and the operator of this site does not guarantee any specific outcome. Do your own reconciliation before committing capital to a price, an ad budget, or a logistics contract.',
    fundingTitle: 'How this site is funded',
    fundingBody:
      'The site is funded by the operator\'s own e-commerce revenue. When ads are enabled, they are Google AdSense non-personalized by default and only run after the visitor has explicitly accepted the cookie banner. The site does not accept sponsored posts, does not run affiliate redirects, and does not sell email lists. The Resources page lists outbound links to a small set of named partners; only those links carry rel="nofollow sponsored" to flag a paid referral, and the disclosure is repeated in the Privacy and Terms pages.',
    partnerLinksTitle: 'Outbound partner links',
    partnerLinksBody:
      'The Resources page lists a small set of named partner links (Shopify, Stripe, PayPal, 17Track, Etsy, Amazon FBA tooling). Only those links carry rel="nofollow sponsored" so the destination sees a paid referral. The site does not run affiliate redirects, does not inject tracking parameters on outbound URLs, and does not insert partner links into article body text. Other outbound links on the site (e.g. from the editorial references and case studies) are not paid referrals.',
    verifiedIdentitiesLabel: 'Verified identities:',
    verifiedIdentitiesValue: ' PGP-signed changelog + published math derivations on this site.',
    knowsAbout: [
      'Cross-border e-commerce pricing',
      'Amazon FBA fee structure',
      'Dimensional weight and CBM calculation',
      'PayPal and Stripe fee optimization',
      'Meta and TikTok advertising ROAS',
      'Independent AI product monetization',
    ],
    personDescription:
      'Independent operator of cross-border e-commerce stores. Author, publisher and sole editor of Crossborder Cost Lab calculators and guides.',
  },
  zh: {
    title: '关于',
    intro:
      '一个免费工具集，专门帮你算清跨境订单里那些看不见的成本，让定价回到利润本身。',
    who:
      '我自己在做面向北美和欧洲的小型独立站。跨境订单的利润极薄，大部分损耗藏在付款手续费、汇差、体积重、广告浪费这些没人给你算清楚的数字里。跨境成本实验室是我把自用的计算器公开出来的地方，省得你再从头搭一遍。',
    forSellers:
      '如果你在 Shopify、WooCommerce、Amazon、TikTok Shop 上卖货，或者做单品 Dropshipping，这个站点就是为你准备的。这些工具假设你清楚自己的货成本、已经在发跨境包裹、想要 30 秒内拿到答案，而不是再读一份 40 页的白皮书。',
    sideProject:
      '副栏：AI 实验跟踪独立 AI 产品——收入规模、商业模式、内容飞轮、常见失败点。案例取自公开文章或公开文件，由本站在第一性分析基础上做摘要。底层算账（毛利、回本、用户终身价值）用的还是跨境计算器同一套数学。',
    principles: [
      '无需注册、无需邮箱——页面打开就能算。',
      '公式公开透明——计算过程可见，假设条件有说明。',
      '不接受付费排序——工具按回答的问题排序，不按付费金额排序。',
    ],
    contact:
      '发现汇率过时、币种缺失，或边角案例下算错了？欢迎邮件到 contact@kuajinglab.xyz 告诉我——每条都会看。',

    editorialTitle: '编辑标准',
    editorialIntro: '本站所有内容遵守四条规则，故意写得很短——重点是可核对。',
    sourcingTitle: '内容来源与生产方式',
    sourcingItems: [
      '工具由第一性公式写出，每个工具在页面底部引用底层费率表（Stripe 价目页、PayPal 费率表、Amazon FBA 计算器输出、承运商体积重表）。',
      'AI 实验栏目的案例，是对公开文章、访谈或文件的摘要改写，每篇首次提到原始来源时都会附链接；若没有可复核的具体 URL，文章会在尾部加一个 `## 来源` 段，明确说明这是运营者阅读过的公开材料的摘要。',
      '表格里的数字（RPM、ARR、费率百分比）按来源原文引用。四舍五入会注明；存在分歧的数字会注明分歧方。',
      '不接代写、不发布未经编辑通过的自动生成文章、不发布未经母语读者复核的机翻内容。',
    ],
    correctionsTitle: '纠错政策',
    correctionsBody:
      '如果某个工具算错了，或某篇文章引用的数字已经过时，收到反馈后 7 天内修复。工具类的修正静默更新（frontmatter 日期同步更新）。文章中的事实错误会在页面底部加日期化的更正说明，保留审核痕迹。',
    reviewCadence: '复核频率',
    reviewBody:
      '每个计算器每季度至少对照原始费率表复核一次。引用动态数字（承运商费率、广告 CPM、AI 产品定价）的文章按同样频率复核并在 frontmatter 标注日期。无法回溯到原始来源进行复核的页面，标记为"过期"或下架。',
    boardTitle: '编辑责任',
    boardIntro:
      '跨境成本实验室由一人运营。为便于问责，下列职责按角色分配，明确谁负责哪一类决策。',
    boardItems: [
      { role: '出版人 & 主编', who: 'kuajinglab', note: '决定发布与撤稿。' },
      { role: '来源核验', who: 'kuajinglab', note: '每季度重新核验所引费率表，发布前终审。' },
      { role: '公式复核', who: 'kuajinglab', note: '每个公式上线前走一遍独立实现对照。' },
      { role: '纠错联系窗口', who: 'kuajinglab', note: '阅读每封来信至 contact@kuajinglab.xyz，持有纠错日志。' },
    ],
    transparencyTitle: '本站不是',
    transparencyBody:
      '跨境成本实验室不是新闻媒体、不是财务顾问、不是税务代理。计算器输出仅为估算；跨境费率结构随时变化，本站运营者不为任何具体结果背书。在把资金押到某个价格、广告预算或物流合同前，请自行核对。',
    fundingTitle: '本站资金来源',
    fundingBody:
      '本站由运营者本人的电商业绩自筹。开启广告时，仅在访客通过 Cookie 横幅明确同意之后，投放 Google AdSense 非个性化广告。本站不接受付费软文、不做联盟跳转倒流、不出售邮件列表。资源页面列出少量明确命名的合作方外链；仅有这些链接会标注 rel="nofollow sponsored" 以告知对方这是一次带佣金的推荐，这一披露同时在隐私政策与服务条款中重复说明。',
    partnerLinksTitle: '外链合作方',
    partnerLinksBody:
      '资源页面列出少量明确命名的合作方链接（Shopify、Stripe、PayPal、17Track、Etsy、亚马逊 FBA 工具）。仅这些链接标注 rel="nofollow sponsored"，以告知对方这是一次带佣金的推荐。本站不做联盟跳转倒流，不在出站 URL 上加追踪参数，也不会在文章正文里插入合作方链接。站内其他外链（编辑参考、案例研究等）均不构成付费推荐。',
    verifiedIdentitiesLabel: '可验证身份：',
    verifiedIdentitiesValue: ' PGP 签名更新日志 + 公开数学推导过程(本站)。',
    knowsAbout: [
      '跨境电商店铺定价',
      'Amazon FBA 费用结构',
      '体积重与 CBM 计算',
      'PayPal / Stripe 费率优化',
      'Meta / TikTok 广告 ROAS',
      '独立 AI 产品变现',
    ],
    personDescription:
      '独立跨境电商店铺运营者。跨境成本实验室计算器与指南的作者、出版人、唯一编辑。',
  },
};
