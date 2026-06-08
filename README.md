# Chestnut 爆款文案三层 Skill

读取文风、套用 Chestnut 爆款文案 SOP、必要时放进公众号草稿箱。

这是一个给中文创作者用的三层 AI 文案 Skill。它会用你的历史文案生成一份属于你的 `文风说明.md`，再用 Chestnut 的爆款文案 SOP 帮你判断选题、打磨封面标题 Hook、检查留存率，最后在需要时把确认好的本地文章放进公众号草稿箱。

## 三层结构

1. **文风分析**
   从你的历史母稿里总结你的个人文案风格，负责判断“像不像你”。推荐用公众号历史文章，因为很多创作者会先把母稿发在公众号；也可以用本地 Markdown、HTML、TXT 或 JSON 文件。

2. **Chestnut 爆款文案 SOP**
   用 Zoe / Chestnut 的文案方法论做选题判断、用户洞察、痛点排序、结构、封面标题 Hook、人味注入、去 AI 味和留存率检查，负责判断“这篇内容有没有传播力”。

3. **公众号发布助手**
   可选发布层。处理标题、摘要、封面检查、公众号草稿箱上传和发布前人工审核，负责“怎么落地”。

## 适合谁

- 内容创作者
- 公众号写作者
- 个人品牌 / 一人公司
- 想把历史文案变成 AI 工作流的人
- 想让 AI 帮忙写母稿，但不想每次重新教文风的人

## 安装

把这个文件夹作为 Skill 放进你的 AI 工具支持的 skills 目录里。

推荐仓库名：

```text
chestnut-copy-skill
```

机器识别的 skill name 是：

```text
chestnut-copy-skill
```

用户看到的名字是：

```text
Chestnut 爆款文案三层 Skill
```

## 配置公众号凭证（可选）

只有当你要读取公众号历史文章，或把文章上传到公众号草稿箱时，才需要配置公众号凭证。

第一次使用前，在本地创建一个不会上传到 GitHub 的密钥文件：

```bash
mkdir -p .secrets
printf '%s\n' \
  'WECHAT_MP_APPID=your_appid' \
  'WECHAT_MP_APPSECRET=your_appsecret' \
  'WECHAT_MP_AUTHOR=your_name' \
  > .secrets/wechat-mp.env
```

脚本会自动读取：

1. `WECHAT_MP_ENV_FILE`
2. `./.env`
3. `./.secrets/wechat-mp.env`
4. skill 目录里的 `.env`
5. skill 目录里的 `.secrets/wechat-mp.env`
6. `~/.wechat-mp.env`

`.secrets/`、`.env`、`outputs/` 已经写进 `.gitignore`，不要把 AppSecret 上传到 GitHub。

## 第一次运行

微信公众平台 API 需要 IP 白名单。第一次正式调用 API 前，先获取当前公网 IP：

```bash
curl -s https://api.ipify.org
```

然后到公众号后台：

```text
设置与开发 -> 基本设置 -> IP 白名单
```

把当前 IP 加进去。

## 读取历史文章并生成文风

读取最新 20 篇已发布文章：

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --count 20 \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

继续读取更早的 20 篇：

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --source published \
  --offset 20 \
  --count 20 \
  --append "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

如果你已经有本地文章文件，也可以不用微信 API：

```bash
python3 -B scripts/fetch_wechat_articles.py \
  --local "/absolute/path/to/article_exports" \
  --output "${STYLE_ANALYZER_ARTICLES:-./outputs/articles.json}"
```

AI 读取生成的 `articles.json` 后，会输出：

```text
./outputs/文风说明.md
```

## 写文案时怎么用

让 AI 读取：

```text
./outputs/文风说明.md
references/chestnut-copy-sop.md
```

然后按三层流程工作：

- 文风分析：像不像你
- Chestnut 爆款文案 SOP：值不值得写、结构强不强、封面标题 Hook 有没有传播力、留存率会不会掉
- 公众号发布助手：标题、摘要、封面、草稿箱、人工审核

## 封面规则

公众号草稿必须有封面。

创建真实草稿前，AI 会先问：

```text
你现在有公众号封面图吗？
如果有，请给我本地图片路径；
如果已经有永久素材 thumb_media_id，也可以直接给 media_id。
没有的话，我先给你封面方向 / AI 生成提示词，等你确认封面后再创建草稿。
```

规则：

- 有本地封面图：用 `--cover`
- 有永久素材 ID：用 `--thumb-media-id`
- 都没有：只给封面方向或 AI 生成提示词，不创建真实草稿

## 放进公众号草稿箱

使用已有永久素材封面：

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

使用本地封面图：

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.html" \
  --cover "/absolute/path/cover.jpg" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

正式创建前可以先 dry run：

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --dry-run
```

## 安全边界

- 默认只创建草稿，不自动发布。
- 不自动群发。
- 不自动定时发布。
- AppSecret 不写进聊天记录、Skill 文件、README 或 GitHub。
- 草稿创建后，请自己去公众号后台或微信文章助手检查排版、图片、标题、摘要和错别字，再手动发布。

## 文件结构

```text
.
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── chestnut-copy-sop.md
│   └── wechat-api.md
└── scripts/
    ├── fetch_wechat_articles.py
    └── publish_draft.py
```

## 常见问题

### 40164 是什么？

当前机器 IP 不在公众号后台 IP 白名单。重新获取公网 IP，并加到公众号后台。

### 这个会自动发布吗？

不会。默认只放进草稿箱，最后发布必须人工审核。

### 没有公众号历史文章可以用吗？

可以。用 `--local` 读取你自己的 Markdown、HTML、TXT 或 JSON 历史文案。

### 这套 SOP 是通用的吗？

它是 Zoe / Chestnut 的爆款文案方法论打包版。用户的文风来自自己的历史文章，文案生产流程使用 Chestnut 的 SOP。
