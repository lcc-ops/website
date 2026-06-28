---
title: '为什么个人站长应该选择「静态优先」'
description: '从实践出发，讲清楚为什么静态优先 + 边缘函数足以覆盖 99% 的个人内容站需求。'
pubDate: 2025-12-10
category: 'architecture'
tags: ['static-site', 'cloudflare-pages', 'seo', 'astro']
translationKey: 'why-static-first'
tldr: '静态优先为独立创作者提供免费托管、最快加载和利于 Google SEO 的页面，无需任何服务器运维。'
faq:
  - q: '我还需要后端吗？'
    a: '只有在纯 HTML/CSS/JS 做不到的时候才需要——比如短链跳转、点击统计、第三方 API 代理。其余都保持静态。'
  - q: 'Cloudflare Pages 真的永久免费吗？'
    a: '静态 + Workers 免费额度内完全免费。只有主动升级到 Workers Paid 才计费，而本站用不到。'
---

「静态优先」意味着服务器直接返回已经渲染好的 HTML 文件，而不是每次请求重新渲染。会带来三个具体收益。

## 性能

- 每次请求省去数据库往返。
- CDN 边缘全球缓存，最近的节点直接响应。
- 即便在弱网下 Core Web Vitals 也能保持绿色。

## 成本

- 没有算力账单，没有数据库账单，没有图片 CDN 账单（Cloudflare 图片缩放是免费的）。
- 免费 SSL、免费 DDoS 防护、免费统计。

## SEO

- 搜索引擎无需执行 JavaScript 即可读取所有页面。
- Schema 和 meta 标签直接烧进 HTML，AI 爬虫可以稳定提取。

## 何时才需要边缘函数

只在纯客户端代码做不到的时候。常见场景：`/go/<id>` 跳转追踪、生成分享短链、按 IP 跳地区化语言。Pages Functions 不需要你维护一台服务器。
