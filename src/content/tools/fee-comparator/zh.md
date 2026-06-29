---
title: 'PayPal vs Stripe 手续费对比器'
description: '输入客单价和月单量，对比 PayPal 与 Stripe 的月手续费总额和有效费率。'
pubDate: 2026-06-30
category: 'payment'
tags: ['paypal', 'stripe', '费率', '对比', '收款', '电商']
icon: '💳'
component: 'FeeComparator'
translationKey: 'fee-comparator'
tldr: 'PayPal 商业交易 4.4% + $0.30；Stripe 标准卡 2.9% + $0.30（含跨境卡约 4.4% 综合费）。PayPal 多收 1.5% 国际费加 3–4% 汇损。'
faq:
  - q: '跨境电商谁更便宜，PayPal 还是 Stripe？'
    a: '直接刷卡场景 Stripe 通常便宜 1–2%。PayPal 在基础费率上叠加 1.5% 国际费，再加 3–4% 汇损（结算到非美元币种）。Stripe 标准国际卡费率 2% + 1.5%，体量上来后用 Adyen 可能更便宜。'
  - q: 'Shopify 最便宜的收款方式？'
    a: 'Shopify Payments（基于 Stripe）通常最便宜——Shopify 在高阶套餐里补贴部分手续费。非 Shopify 站点，Stripe 标准 2.9% + $0.30 仍很有竞争力。PayPal Payflow Pro 在 PayPal 费率基础上每笔再加 $0.10。'
  - q: '怎么避免 PayPal 和 Stripe 的拒付？'
    a: '两家都支持 3DS 验证，全场景开启。Stripe Radar（免费）用机器学习拦截可疑卡；PayPal Seller Protection 在按验证地址发货并提供物流单号时覆盖欺诈申诉。完整 SOP 见 [拒付预防](/zh/content/payment-chargeback-prevention/)。'
  - q: 'PayPal 有月费吗？'
    a: '标准商业账户无月费。PayPal 国内商业交易 4.4% + $0.30，跨境再加 1.5%，提现若换币种再加 3–4% 汇损。小额账户（<$10）单独定价 5% + $0.05。'
  - q: 'Stripe 怎么处理货币转换？'
    a: 'Stripe 按客户本币扣款，按银行间汇率 + 1% 换成结算币种。要保留原币，开启多币种结算——Stripe 会在 USD/EUR/GBP/JPY 等账户余额中免手续费持有。'
  - q: '能同时用 PayPal 和 Stripe 吗？'
    a: '可以。Shopify、WooCommerce、BigCommerce 都支持。同时 A/B 测试两种方式对结账转化的影响——年长欧盟消费者、B2B 客户偏好 PayPal 或对公转账，年轻移动端偏好数字钱包。'
---

PayPal 和 Stripe 在标准卡交易上都收大约 **3% + $0.30**，但一旦叠加国际卡、货币转换、拒付费，结构差异立刻拉开。一个 $35 客单价 × 300 单/月的店铺，月流水 $10,500——1% 有效费率差就是 $1,260/年。

## 计算器怎么算

1. **客单价 (USD)**——平均订单金额。
2. **月单量**——每月订单总数。

输出：

- 各家**月手续费**
- **有效费率** = 月手续费 ÷ 月流水
- **差额**——按月的金额差

默认假设 **PayPal 商业交易**（4.4% + $0.30）和 **Stripe 标准卡**（2.9% + $0.30 基础，含约 1.5% 跨境卡附加作为综合有效费率）。按自己的实际客单组成调整。

## 不同订单量的有效费率

| 客单价 | 月单量 | 流水 | PayPal 费 | Stripe 费 | 月差 | 年差 |
|---|---|---|---|---|---|---|
| $25 | 200 | $5,000 | $280 | $194 | $86 | $1,032 |
| $35 | 300 | $10,500 | $569 | $404 | $165 | $1,980 |
| $60 | 500 | $30,000 | $1,590 | $1,140 | $450 | $5,400 |
| $120 | 150 | $18,000 | $948 | $696 | $252 | $3,024 |

差额与**流水**大致线性相关，与单数无关。$30k/月流水，PayPal 多收 ~$5,400/年——在某些市场够一个全职员工。Stripe 在标准国内卡场景胜出；PayPal 只在买家明确拒绝刷卡的场景才赢。

## 这工具不算什么

- **拒付 / 争议费**（每笔 $15–20）——预留准备金。
- **订阅计费折扣**——Stripe Billing 和 PayPal Subscriptions 的留存卡定价不一样。
- **本地支付**（iDEAL、Klarna、Alipay）——Adyen、Mollie、Airwallex Payment Acceptance 等聚合器用一笔费率包打。
- **刷卡 vs 输卡**——POS 与线上定价不同。

## 常见错误

- **把"无月费"等同于免费**——PayPal 无月费但单笔费率更高，跑数看看。
- **忽略 1.5% 国际附加费**——在基础费率上叠加。PayPal 跨境交易 4.4% + 1.5% = 5.9%，还没算汇损。
- **忘记货币转换**——客户付 EUR、你结算 USD，PayPal 在公示汇率上再加 3–4%。Stripe 是 1%。
- **低估拒付**——准备 0.1–0.3% 流水的准备金；高客单品类（电子、保健品）可能到 1%。

## 何时切换服务商

- **<$50k/月 + 纯国内**：Stripe 通常便宜 0.5–1%。PayPal 的支票罕见。
- **跨境销售**：Stripe 银行间汇率比 PayPal 内嵌汇损便宜 1–2%。
- **B2B 或年长欧盟客户**：Stripe 为主，PayPal 留为备用——结账转化常常提升。
- **订阅业务**：Stripe Billing 的留存卡费率显著低于 PayPal Subscriptions（规模化后）。
- **要本地支付方式**（iDEAL、Bancontact、BLIK）：用 Adyen 或 Mollie，不要直接 PayPal/Stripe。

## 何时这工具不够用

- **量级定价** $100k+/月启动——联系两家拿定制费率；本计算器按公示费率算。
- **平台专属费率**（Etsy Payments、Amazon Seller Central）有自家定价表。
- **加密或 BNPL**（Klarna、Afterpay）在 PayPal 和 Stripe 标准定价之外。

## 工作流

1. 从你店铺后台拉最近 90 天流水和单数。
2. 用**实际**客单价（中位数，不是标价）跑本计算器。
3. 用上方「有效费率」表交叉核对所在流水段。
4. 决定切换前，做 30 天 Stripe Checkout A/B 测试再全量迁移。

## 配套阅读

- **[定价计算器](/zh/tools/pricing-calculator/)**——把有效费率回灌利润率
- **[汇率与提现对比器](/zh/tools/fx-withdraw-calculator/)**——测提现后实际到账
- **[ROAS 计算器](/zh/tools/roas-calculator/)**——把有效费率算进广告保本
- **深度文章**——[PayPal vs Stripe 费率详解](/zh/content/paypal-vs-stripe-fees/)