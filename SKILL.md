---
name: chestnut-copy-skill
description: >
  Three-layer Chestnut Copy skill package. Use when a creator wants to analyze
  their own writing voice from historical writing samples (WeChat recommended),
  use Zoe/Chestnut's copywriting SOP to turn ideas into stronger drafts, and
  optionally send a local Markdown/HTML article to the WeChat Official Account
  draft box. Default assumption: the user's writing samples provide their voice
  layer, Chestnut Copy provides the production method, and WeChat upload is an
  optional publishing helper. Supports Claude Code, Codex, and WorkBuddy through
  local secret files, environment variables, and bundled Python scripts.
---

# Chestnut 爆款文案三层 Skill

## What This Skill Does

This is a packaged Chestnut Copy workflow for other creators. It has three layers:

1. **文风分析**: read the user's historical writing samples and summarize their personal voice. WeChat historical articles are recommended because many creators use them as mother drafts, but local files also work.
2. **Chestnut 爆款文案 SOP**: use Zoe/Chestnut's copy production method to turn ideas into publishable mother drafts and platform versions.
3. **公众号发布助手**: optionally send a finished local Markdown or HTML mother draft to the WeChat Official Account draft box.

Default to this persistent workflow. Do not treat credentials as a one-off value the user must paste every new chat.

## Cross-Environment Rule

This skill must work in Claude Code, Codex, and WorkBuddy. Use only:

- local files,
- environment variables,
- untracked local secret files,
- bundled scripts inside this skill directory.

Do not rely on machine-specific memory folders, hidden app state, or another skill being installed.

## Long-Term WeChat Credential Setup

Only needed for the 公众号发布助手 layer or live WeChat article fetching. Default credential storage is a local untracked file:

```bash
mkdir -p .secrets
printf '%s\n' \
  'WECHAT_MP_APPID=your_appid' \
  'WECHAT_MP_APPSECRET=your_appsecret' \
  'WECHAT_MP_AUTHOR=your_name' \
  > .secrets/wechat-mp.env
```

The scripts automatically read credentials from:

1. `WECHAT_MP_ENV_FILE`
2. `./.env`
3. `./.secrets/wechat-mp.env`
4. the same files inside this skill directory
5. `~/.wechat-mp.env`

Real environment variables override file values. The secret files are ignored by `.gitignore`; never commit them.

If a user has already configured credentials, do not ask again. Run the scripts and let their error output tell you if credentials are missing or invalid.

## First-Time Live API Check

Only needed before the first real WeChat API call from a new machine/network:

```bash
curl -s https://api.ipify.org
```

Tell the user:

`当前机器公网 IP 是 [IP]，请先在公众号后台（设置与开发 -> 基本设置 -> IP 白名单）添加这个 IP，完成后告诉我继续。`

Wait for confirmation. If an API call later fails with `40164`, the IP is not allowlisted.

## 三层结构

Keep these separate:

- **1. 文风分析**: the user's own voice, opening logic, sentence rhythm, recurring expressions, anti-AI rules, and how they turn experience into观点. Responsible for: "does this sound like the creator?"
- **2. Chestnut 爆款文案 SOP**: Zoe's copy production method: topic gate, audience insight, pain-point sorting, structure, cover/title/hook decision, retention check, human texture, AI-flavor removal, spreadability, and platform adaptation. Responsible for: "does this have spreadability?"
- **3. 公众号发布助手**: title, digest, cover decision, WeChat draft-box workflow, and manual backend review. Responsible for: "how does this land?"
- **公众号排版格式**: 小三角 `▼`, section spacing, headings, line breaks, cover, images, HTML structure. Record these, but do not confuse them with voice.
- **平台改写格式**: after the mother draft exists, adapt it into video script, RedNote caption, YouTube description, or other platform forms without changing the underlying copy voice.

This skill analyzes and stores **个人文案风格** first. Then it uses the Chestnut Copy SOP as the production layer. Do not overfit the writing voice to visual layout symbols.

## Source Selection

Default source for style analysis:

- `published`: historical published articles through `freepublish/batchget`.

Use only when explicitly needed:

- `draft`: draft-box articles through `draft/batchget`.
- `local`: exported Markdown, HTML, TXT, or JSON article files.

Read `references/wechat-api.md` for endpoint details and common errors.

Read `references/chestnut-copy-sop.md` when writing, rewriting, evaluating, or adapting copy. This is Zoe/Chestnut's packaged copy method for public users.

If this skill is used inside Zoe's AI Workshop and `chestnut-copy` is installed, use the installed `chestnut-copy` skill instead of this packaged reference, passing the generated `文风说明.md` as voice context.

## Scripts

Fetch or normalize articles:

```bash
python3 -B scripts/fetch_wechat_articles.py
```

Create WeChat draft from a local article:

```bash
python3 -B scripts/publish_draft.py
```

Use `python3 -B` when possible so Python does not write cache files in restricted app environments.

## Workflow A: Configure Once

1. Ask the user for AppID/AppSecret only if no local credential file exists and the script reports missing credentials.
2. Put credentials in `.secrets/wechat-mp.env`.
3. Never paste credentials into `SKILL.md`, reference files, examples that will be committed, or chat summaries.
4. Confirm `.gitignore` includes `.secrets/`, `.env`, `outputs/`, downloaded article JSON, and generated private style guides.

## Workflow B: 文风分析

Fetch latest 20 published articles:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --count 20 \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Fetch more historical articles:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --offset 20 \
  --count 20 \
  --append "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Local fallback:

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --local "/absolute/path/to/article_exports" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

Then read the JSON and produce the user's reusable style guide:

```text
${STYLE_ANALYZER_OUTPUT:-./outputs/文风说明.md}
```

If `文风说明.md` already exists, load it first and refresh it instead of starting from zero, unless the user asks for a full rebuild. Treat it as the user's voice layer for all copy, not only WeChat articles.

## Workflow C: Chestnut 爆款文案 SOP

When the user asks to write, rewrite, evaluate, or adapt copy:

1. Load `./outputs/文风说明.md` or `STYLE_ANALYZER_OUTPUT`.
2. Read `references/chestnut-copy-sop.md`.
3. Apply the three layers:
   - 文风分析: `文风说明.md`, responsible for "does this sound like the creator?",
   - Chestnut 爆款文案 SOP: `chestnut-copy-sop.md`, responsible for "does this have spreadability, a strong cover/title/hook, and enough retention pull?",
   - 公众号发布助手: title, digest, cover decision, WeChat draft-box workflow, and manual review, responsible for "how does this land?"
4. Keep writing voice separate from WeChat layout and platform packaging.
5. Ask before sending to WeChat draft box unless the user explicitly says to create the draft now.

For Zoe/Chestnut only: if the installed `chestnut-copy` skill is available, use it as the SOP layer instead of `chestnut-copy-sop.md`.

## Workflow D: 公众号发布助手

Use after the mother draft is final enough to inspect in the WeChat backend.

Before creating a real draft, ask the cover question:

`你现在有公众号封面图吗？如果有，请给我本地图片路径；如果已经有永久素材 thumb_media_id，也可以直接给 media_id。没有的话，我先给你封面方向 / AI 生成提示词，等你确认封面后再创建草稿。`

Rules:

- Do not assume an AI-generated cover exists.
- Do not create a real WeChat draft without either `--cover` or `--thumb-media-id`.
- If the user has no cover yet, provide cover directions or image-generation prompts and run only `--dry-run` if needed.
- If the user provides a local cover file, upload it as permanent material through `--cover`.
- If the user provides an existing permanent material ID, use `--thumb-media-id`.

With an existing permanent cover `thumb_media_id`:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

With a local cover image:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.html" \
  --cover "/absolute/path/cover.jpg" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

Use `--dry-run` before a live draft when checking fields:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --dry-run
```

Default boundary: create draft only. Do not publish, mass-send, or schedule unless the user explicitly asks and reconfirms.

## 文风说明 Output Format

```markdown
# 个人文案风格说明 v[N]
> 基于 [N] 篇文章分析
> 分析时间：YYYY-MM-DD
> 来源：[published / draft / local]
> 公众号名称：[如 API 可得；否则写未知]

## 这份个人文风适合什么
[creator copy in general: 公众号母稿 / newsletter / 视频脚本母稿 / 小红书文案 / YouTube/B站描述 / caption / launch copy]

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
- 如何从具体经验升到价值观 / 哲学：[描述]
- 幽默或自嘲方式：[描述]

## AI 腔禁区
- 不使用的词 / 句式：[列举]
- 太工整、太模板、太像总结稿的写法：[描述]
- 修改检查规则：[列举]

## 不属于文风、属于排版格式的东西
- 小三角 / 分隔符：[记录但不要当作文案声音]
- 标题层级 / HTML / 图片：[记录到排版层]

## 跨平台改写原则
- 公众号母稿 -> 视频脚本：[怎么保留观点、压缩解释、增加口播节奏]
- 公众号母稿 -> 小红书/RedNote：[怎么变成短标题、封面钩子、caption]
- 公众号母稿 -> newsletter / 社群：[怎么调整开头和 CTA]

## 示例对比
### 符合该风格
> [短例子]

### 不符合该风格
> [短例子，并说明为什么]
```

## Quality Bar

- If fewer than 5 articles are available, state: `样本量偏少，建议增加阅读量以获得更准确的文风画像。`
- Keep examples short. Do not reproduce full articles.
- The final guide must be usable for future copywriting without requiring the creator to paste their style again.
- Public users should use `references/chestnut-copy-sop.md` as the packaged Chestnut Copy method. Zoe's local workspace can substitute the installed `chestnut-copy` skill for the most current Chestnut-specific production rules.
- Always tell the user that WeChat drafts still need manual backend inspection before publishing.
