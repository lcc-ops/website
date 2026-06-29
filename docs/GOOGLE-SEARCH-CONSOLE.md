# Google Search Console 接入

让 Google"认得"你站点的免费工具。完成接入后能看：哪些页面被 Google 收录、哪些关键词带来点击、抓取错误。

---

## 1. 一次性接入（首次添加属性）

### 1.1 打开 GSC

访问 <https://search.google.com/search-console>，用 Google 账号登录。

### 1.2 添加属性

- 选 **URL 前缀**（推荐，验证更快）
- 输入 `https://kuajinglab.xyz/`
- 点 **继续**

### 1.3 验证域名所有权

GSC 给出 4 种验证方式。**本项目推荐 HTML 文件法**：

| 方式 | 难度 | 适合 |
|---|---|---|
| **HTML 文件**（推荐） | 1 分钟 | 任何项目，把文件丢 public/ 就行 |
| HTML meta 标签 | 2 分钟 | 想塞 BaseHead 的项目 |
| Google Analytics | 即时 | 已有 GA 账户 |
| 域名 DNS 记录 | 5 分钟 | 想用 Google 之外的工具验证时 |

**HTML 文件法步骤：**

1. GSC 页面点 **下载档案** → 浏览器下载 `google<随机串>.html`
2. 把这个文件原样放进 `public/google<随机串>.html`
3. `pnpm build`（确保文件进 `dist/`）
4. `git add public/google<随机串>.html` + 提交 + push
5. 等待 Worker 部署完成（约 30–60 秒）
6. 回到 GSC 页面点 **验证** → 应显示 **所有权已验证**

**重要：**
- 验证文件**不能删**。一旦删除，下次重新验证要重新走流程
- 验证文件不要放在子目录，只能放 `public/` 根（最终路径必须是 `https://kuajinglab.xyz/google<随机串>.html`）
- 改域名后**所有验证会失效**，要在 GSC 重新加新属性

---

## 2. 提交 sitemap

sitemap 告诉 Google 你站点有哪些页面，**不提交 = Google 不知道你文章存在**，只能等 Google 慢慢爬内链。

### 2.1 找到 sitemap URL

Astro 配 `@astrojs/sitemap` 后，build 自动生成：

```
https://kuajinglab.xyz/sitemap-index.xml
```

打开确认能访问。里面是 sitemap 列表，每个子 sitemap 列出实际页面 URL。

### 2.2 提交

1. GSC 左侧菜单 → **Sitemaps**
2. 输入框填 `sitemap-index.xml`
3. 点 **提交**
4. 状态会在几小时内从"待处理"变"成功"

---

## 3. 何时重新提交 sitemap

sitemap 提交一次后**会一直生效**——Astro 每次 build 都会刷新 `dist/sitemap-index.xml`，GSC 会按 `lastmod` 字段识别新内容。

**不需要每次发文章都重提。** 建议重新提交的时机：

| 时机 | 原因 |
|---|---|
| 域名改了 | sitemap 里的 URL 全是旧域 |
| 大量一次性删除页面 | 触发抓取预算重新计算 |
| 全新子域 / 全新属性 | 第一次接入 |
| 站点迁移到新平台 | URL 结构变了 |

平时发新文章 → GSC 在下次抓取时自动发现，不需要手动操作。

---

## 4. 提交个别 URL 强制抓取

如果你刚发了一篇重要文章，等不及 Google 自然抓取：

1. GSC 顶部 → **URL 检查**
2. 输入完整 URL（例：`https://kuajinglab.xyz/content/new-post`）
3. 点 **请求编入索引**

每日有配额限制（约 10–12 个 URL），别滥用。

---

## 5. 关注什么

接入后第一周看这几项：

| 位置 | 指标 | 怎么看 |
|---|---|---|
| **覆盖范围** | 已编入索引的页面数 | 是不是匹配 sitemap 条目数 |
| **覆盖范围** | 排除项 | 是否有大量 `noindex` / 404 / 重复 |
| **效果** → **搜索结果** | 点击次数、展示次数 | 哪些文章有曝光 |
| **效果** → **搜索结果** → **查询** | 关键词 | 用户搜什么词找到你 |
| **抓取** → **抓取统计** | 抓取请求 / 响应 | Worker 是否有错误 |

---

## 6. 常见问题

| 症状 | 原因 |
|---|---|
| 验证一直失败 | 文件没 push / Worker 没部署 / 路径不对 |
| sitemap 状态"无法获取" | 路径写错 / 域名不匹配 / 服务器 500 |
| 索引数远小于 sitemap | 新站正常，需要 2–4 周持续抓取 |
| 域名换后旧 GSC 属性失效 | 新域名要重新加属性 + 重新验证 |

---

## 7. 与本站其他流程的衔接

| 任务 | 关联 |
|---|---|
| 发新文章 | `docs/NOTES.md` § 7 上线流程 |
| 换域名 | `docs/NOTES.md` § 9 域名切换 |
| AdSense 接入 | 申请 AdSense 之前先做 GSC 接入，让 Google 信任你站 |
