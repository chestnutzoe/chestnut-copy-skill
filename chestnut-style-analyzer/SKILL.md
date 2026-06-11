---
name: chestnut-style-analyzer
description: Use when a creator wants to analyze their own writing voice from historical copy, especially WeChat Official Account articles or local Markdown, HTML, TXT, or JSON exports, and produce a reusable style guide for future copywriting.
---

# 文风分析

## Purpose

This skill turns a creator's historical writing into a reusable `文风说明.md`.

It answers one question:

> 这篇文案像不像这个人？

It is independent, but works best as the first layer of the Chestnut Copy skill set:

1. 文风分析: extract the creator's voice.
2. Chestnut 爆款文案 SOP: use Zoe/Chestnut's production method.
3. 公众号发布助手: upload approved drafts to the WeChat draft box.

## Source Rule

Recommended source: WeChat Official Account historical articles, because many Chinese creators use WeChat as the mother-draft archive.

Also support local writing samples:

- Markdown
- HTML
- TXT
- JSON exports

Keep voice separate from publishing format. Symbols such as `▼`, section spacing, cover style, title hierarchy, and HTML layout belong to the layout layer, not the voice layer.

## Credential Setup

Only needed for live WeChat fetching. If the user uses local files, no credential is needed.

Use persistent local credentials by default. The script reads:

1. `WECHAT_MP_ENV_FILE`
2. `./.env`
3. `./.secrets/wechat-mp.env`
4. the same files inside this skill directory
5. `~/.wechat-mp.env`

Existing environment variables win over file values.

Never commit AppID, AppSecret, access tokens, downloaded article JSON, or generated private style guides.

## First Live API Check

Before a real WeChat API call from a new network, get the current IP:

```bash
curl -s https://api.ipify.org
```

Tell the user to add it in:

```text
公众号后台 -> 设置与开发 -> 基本设置 -> IP 白名单
```

If the API returns `40164`, the current IP is not allowlisted.

## Fetch Writing Samples

Fetch latest 20 published WeChat articles:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --count 20 \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Fetch older articles:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --offset 20 \
  --count 20 \
  --append "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Use local files:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --local "/absolute/path/to/article_exports" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Use `python3 -B` so Python does not write cache files in restricted app environments.

Read `references/wechat-api.md` only when endpoint details or WeChat errors matter.

## Produce The Style Guide

After reading `articles.json`, create or refresh:

```text
${STYLE_ANALYZER_OUTPUT:-./outputs/文风说明.md}
```

If `文风说明.md` already exists, load and refresh it instead of starting from zero, unless the user requests a rebuild.

## Output Format

```markdown
# 个人文案风格说明 v[N]
> 基于 [N] 篇文章分析
> 分析时间：YYYY-MM-DD
> 来源：[published / draft / local]
> 公众号名称：[如 API 可得；否则写未知]

## 这份个人文风适合什么
[公众号母稿 / newsletter / 视频脚本母稿 / 小红书文案 / YouTube/B站描述 / caption / launch copy]

## 核心风格关键词
[3-5 个关键词]

## 开头习惯
[2-3 种真实开头逻辑，各附短例子]

## 句子和段落节奏
- 句子长度：[描述]
- 段落长度：[描述]
- 留白节奏：[描述]

## 常用表达
- 高频句式：[列举]
- 语气词 / 标点偏好：[列举]
- 中英混用：[如有]

## 思想和情绪结构
- 常见推进方式：[描述]
- 如何从具体经验升到观点 / 价值观：[描述]
- 幽默或自嘲方式：[描述]

## AI 腔禁区
- 不使用的词 / 句式：[列举]
- 太工整、太模板、太像总结稿的写法：[描述]
- 修改检查规则：[列举]

## 不属于文风、属于排版格式的东西
- 小三角 / 分隔符：[记录但不要当作文案声音]
- 标题层级 / HTML / 图片：[记录到排版层]

## 跨平台改写原则
- 公众号母稿 -> 视频脚本：[保留观点、压缩解释、增加口播节奏]
- 公众号母稿 -> 小红书/RedNote：[短标题、封面钩子、caption]
- 公众号母稿 -> newsletter / 社群：[调整开头和 CTA]

## 示例对比
### 符合该风格
> [短例子]

### 不符合该风格
> [短例子，并说明为什么]
```

## Quality Bar

- If fewer than 5 samples are available, state: `样本量偏少，建议增加阅读量以获得更准确的文风画像。`
- Keep examples short. Do not reproduce full articles.
- The final guide must be usable for future copywriting without requiring the creator to paste their style again.
- Treat the guide as general copy voice, not only WeChat voice.
