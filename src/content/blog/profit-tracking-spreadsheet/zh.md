---
title: '跨境电商利润核算 Excel 搭建教程'
description: '手把手教你用 Excel 或 Google Sheets 搭建利润核算表。含公式、看板配置、免费模板下载。'
pubDate: 2026-06-30
category: 'ops'
tags: ['excel', '表格', '利润', '核算']
translationKey: 'profit-tracking-spreadsheet'
tldr: '利润核算表需要四张 sheet：订单、成本、广告、看板。看板用 SUMIFS 公式按商品、渠道、月份汇总净利润。'
faq:
  - q: '利润核算表要哪些列？'
    a: '订单 sheet：日期、订单号、渠道、SKU、数量、售价、货币、支付费、物流费、产品成本。广告 sheet：日期、渠道、活动、花费、点击、转化、转化价值。看板 sheet 用 SUMIFS 汇总。'
  - q: 'Google Sheets 怎么算利润？'
    a: '净利润 = 收入 − 产品成本 − 物流费 − 支付费 − 广告支出 − 退款成本。用 SUMIFS 按商品、渠道、月份汇总每个成本项。'
  - q: '按 SKU 还是按订单追踪利润？'
    a: '两个都做。按 SKU 看哪些产品赚钱；按订单看个别高成本异常（退款、部分退款、拒付）。'
  - q: '利润表多久更新一次？'
    a: '广告和订单每天更新（15 分钟）。每周和银行/支付平台对账（1 小时）。每月按产品复盘净利（2 小时）。'
  - q: 'Google Sheets 还是 Excel 更适合电商核算？'
    a: 'Google Sheets 胜在协作和免费。Excel 胜在功能（Power Query、数据透视表、Power BI 集成）。个人卖家 Google Sheets 够用。'
---

多数卖家追踪营收但不追踪利润。利润才是你真正留下的。下面是怎么搭建说真话的表格。

## 你需要四张 sheet

完整的利润追踪表有四张 sheet：

### 1. 订单（输入）

每笔销售一行。

| 列 | 描述 |
|---|---|
| date | 下单日期 |
| order_id | 唯一订单号 |
| channel | Shopify、Etsy、Amazon 等 |
| sku | 商品标识 |
| qty | 数量 |
| sale_price | 单价 |
| currency | USD、EUR、GBP |
| payment_fee | Stripe/PayPal 收的 |
| shipping_cost | 物流成本 |
| product_cost | 供应商成本（分摊） |
| shipping_country | 目的地国家 |
| customer_email | 复购分析 |
| status | paid、refunded、partially_refunded |
| refund_amount | 退款金额 |
| chargeback_flag | TRUE/FALSE |
| notes | 备注 |

### 2. 成本（输入）

每单变动的成本。

| 列 | 描述 |
|---|---|
| date | 成本日期 |
| type | shipping、packaging、label、customs、duty 等 |
| amount | 成本 |
| related_order_id | 关联订单号 |
| notes | 说明 |

### 3. 广告（输入）

每日广告花费和结果数据。

| 列 | 描述 |
|---|---|
| date | 花费日期 |
| channel | Google、Meta、TikTok、Pinterest |
| campaign | 广告活动名 |
| spend | 日花费 |
| clicks | 点击数 |
| conversions | 转化数（来自平台） |
| conversion_value | 归因收入（来自平台） |

### 4. 看板（输出）

从其他三张 sheet 通过公式拉数据。更新一次，看到全部。

## 关键公式

### 按月总营收

```
=SUMIFS(Orders!F:F, Orders!A:A, ">="&DATE(2026,1,1), Orders!A:A, "<"&DATE(2026,2,1))
```

### 按商品净利（最近 30 天）

```
=SUMIFS(Orders!F:F, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!I:I, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!H:H, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30) -
 SUMIFS(Orders!G:G, Orders!D:D, "SKU-001", Orders!A:A, ">="&TODAY()-30)
```

F 是收入，I 是产品成本，H 是物流成本，G 是支付费。

### 净利率 %

```
=net_profit_cell / total_revenue_cell
```

### 按渠道 ROAS（最近 30 天）

```
=SUMIFS(Ads!F:F, Ads!B:B, "Google", Ads!A:A, ">="&TODAY()-30) /
 SUMIFS(Ads!D:D, Ads!B:B, "Google", Ads!A:A, ">="&TODAY()-30)
```

### 广告驱动单件利润（Google，最近 30 天）

```
=(SUMIFS(Ads!F:F, ...) / SUMIFS(Ads!E:E, ...)) -
 SUMIFS(Orders!I:I, ...) / COUNTIFS(...)
```

## 看板布局

```
┌─────────────────────────────────────────────────────────┐
│  跨境利润看板 — 最近 30 天                              │
├─────────────────────────────────────────────────────────┤
│  营收：              $X,XXX     ▲ X% vs 上 30 天       │
│  净利润：            $XXX       ▼ X% vs 上 30 天        │
│  净利率：            XX.X%                                │
│  广告支出：          $XXX       ROAS: X.X×               │
│  客单价：            $XX.X      订单数：XXX              │
├─────────────────────────────────────────────────────────┤
│  按 SKU 利润                                          │
│  SKU-001   $XXX   XX% 利润率   ████████████            │
│  SKU-002   $XXX   XX% 利润率   █████████               │
│  SKU-003   -$XX   -XX% 利润率  ██                      │
│  ...                                                    │
├─────────────────────────────────────────────────────────┤
│  按渠道利润                                            │
│  Shopify  $XXX    Etsy  $XXX    Amazon  $XXX           │
├─────────────────────────────────────────────────────────┤
│  主要支出（最近 30 天）                                │
│  广告       $XXX  营收 XX%                              │
│  物流       $XXX  营收 XX%                              │
│  支付费     $XXX  营收 XX%                              │
│  产品成本   $XXX  营收 XX%                              │
│  退款       $XXX  营收 XX%                              │
└─────────────────────────────────────────────────────────┘
```

## 实施步骤

1. **建四张 sheet**，表头按上面来。
2. **每天导入订单** — Shopify、Etsy、Amazon 都能导 CSV。用脚本或手动导入。
3. **每天导入广告** — Google Ads API、Meta API，或 CSV 导出。
4. **在看板 sheet 配一次公式**，自动更新。
5. **加条件格式** — 赚钱绿色，亏钱红色。
6. **每周邮件摘要** — Google Sheets 能把看板发邮件附件。

## 常见坑

### 货币混用

同一营收列别混 USD 和 EUR。两个办法：

- 全部按销售日汇率换算成 USD（用日汇率）
- 分列存，月末统一换算

### 产品成本分摊

卖组合装或多件装，按 SKU 分摊成本。别把整套供应商成本压在一个 SKU 上。

### 退款追踪

退款不冲销原始成本。在成本 sheet 里加一行，退款金额作为负营收。

### 不退的退货

有些客户保留商品拿部分退款。作为单独成本行，不是退款。

### 广告归因

平台报的转化常常和你的订单数据对不上。ROAS 用平台报的数据，但每月和银行流水对账。

## 自动化数据流

### Shopify → Google Sheets

用 Shopify API + Google Apps Script，或：

- **Matrixify** — 批量导入导出
- **Shopify Google Sheets 插件** — 直接同步
- **Zapier** — 订单触发新行

### 广告 → Google Sheets

- **Google Ads API + Apps Script** — 每日拉取
- **Supermetrics** — 付费但稳定
- **手动 CSV 导出** — $10k/月个人卖家够用

### 银行 → Google Sheets

多数银行没直连。手动每周对账小卖家够用。

## 什么时候表格不够用

~月营收 $50k 时你需要：

- **库存追踪** — 表格没法实时追踪库存
- **多货币** — 多银行账户、多供应商付款
- **COGS 准确度** — 每票货的落地成本
- **渠道专属费** — 亚马逊 FBA 仓储费、Etsy 广告费等

升级到：

- **A2X + Google Sheets** — Shopify 之上的会计层
- **QuickBooks Online** — 基础但稳
- **Xero** — 国际化更好
- **Cin7 或 DEAR** — 全库存 + 会计

$50k/月以下卖家，维护好的表格胜过这些。

## 下载模板

下载我们免费的 [利润核算 Excel 模板](/zh/resources/) — Google Sheets 或 Excel 都能直接用。