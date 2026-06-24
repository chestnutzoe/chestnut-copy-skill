# Chestnut Copy Skill Set

这是 Zoe / Chestnut 的中文创作者文案 Skill 套装。

它是一个统一的 `chestnut` Claude Code plugin，里面包含多个 Chestnut skills。手动安装时，这些 skill 也可以单独复制使用：

| Skill 文件夹 | 中文名 | 负责什么 | 可以单独用吗 |
| --- | --- | --- | --- |
| `style-analyzer/` | 文风分析 | 从公众号历史文章或本地文案里总结个人文风，生成 `文风说明.md` | 可以 |
| `copy-sop/` | 爆款文案 SOP | 用 Zoe/Chestnut 的方法做选题、洞察、结构、封面标题 Hook、留存率和去 AI 味 | 可以 |
| `wechat-publisher/` | 公众号发布 | 处理标题、摘要、封面预检、API/IP 前置检查，并把确认后的文章上传到公众号草稿箱 | 可以 |

## 推荐使用方式

完整流程：

```text
文风分析 -> 爆款文案 SOP -> 公众号发布
```

三层分工：

1. **文风分析**
   负责“像不像你”。推荐读取公众号历史母稿，也支持本地 Markdown、HTML、TXT、JSON 文案。

2. **爆款文案 SOP**
   负责“有没有传播力”。重点是选题判断、用户洞察、痛点、结构、封面标题 Hook、人味注入、去 AI 味、留存率检查。

3. **公众号发布**
   负责“怎么落地”。重点是标题、摘要、封面、公众号 API 配置检查、IP 白名单检查、草稿箱上传和发布前人工审核。

## 文件结构

```text
.
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── chestnut/
│       ├── .claude-plugin/plugin.json
│       └── skills/
│           ├── style-analyzer/
│           ├── copy-sop/
│           └── wechat-publisher/
├── LICENSE
├── README.md
├── style-analyzer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/wechat-api.md
│   └── scripts/fetch_wechat_articles.py
├── copy-sop/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/chestnut-copy-sop.md
└── wechat-publisher/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/wechat-api.md
    └── scripts/publish_draft.py
```

## Installation

### Via Claude Code Custom Marketplace Source

Install directly from this public GitHub repo. Run these as separate Claude Code messages; do not paste all lines into the prompt at once.

First add this repository as a marketplace source:

```text
/plugin marketplace add https://github.com/chestnutzoe/chestnut-copy-skill
```

Then install the Chestnut plugin:

```text
/plugin install chestnut@chestnut
```

This installs the current Chestnut skill suite, including:

```text
style-analyzer
copy-sop
wechat-publisher
```

Future Chestnut skills can be added under the same `chestnut` plugin, so users keep one clear namespace.

Use the HTTPS URL. The shorter `chestnutzoe/chestnut-copy-skill` form may make Claude Code try SSH, which can fail if GitHub is not already in your `known_hosts` file.

After plugin installation, Claude Code namespaces skills as:

```text
/plugin-name:skill-name
```

For example:

```text
/chestnut:style-analyzer
/chestnut:copy-sop
/chestnut:wechat-publisher
```

If installed manually as standalone skills, use the skill names without plugin namespaces.

### Download This Repo

你可以用两种方式拿到文件：

1. GitHub 页面点击 **Code -> Download ZIP**，解压后选择要安装的 skill 文件夹。
2. 用命令行 clone：

```bash
git clone https://github.com/chestnutzoe/chestnut-copy-skill.git
cd chestnut-copy-skill
```

这个仓库同时支持 Claude Code plugin 安装和手动 skill 安装。手动安装时，真正的 skill 文件夹是：

```text
style-analyzer/
copy-sop/
wechat-publisher/
```

每个文件夹都可以单独复制到你的 AI 工具 skills 目录里。

### Fast Install For Claude Code

如果你想一次装完三个 skill，可以直接运行：

```bash
git clone https://github.com/chestnutzoe/chestnut-copy-skill.git /tmp/chestnut-copy-skill
mkdir -p ~/.claude/skills
cp -R /tmp/chestnut-copy-skill/style-analyzer ~/.claude/skills/
cp -R /tmp/chestnut-copy-skill/copy-sop ~/.claude/skills/
cp -R /tmp/chestnut-copy-skill/wechat-publisher ~/.claude/skills/
```

如果你之后重新下载，先删除 `/tmp/chestnut-copy-skill` 或换一个临时目录。

### Install All Three For Claude Code

把三个 skill 都装到 Claude Code：

```bash
mkdir -p ~/.claude/skills
cp -R style-analyzer ~/.claude/skills/
cp -R copy-sop ~/.claude/skills/
cp -R wechat-publisher ~/.claude/skills/
```

安装后，在 Claude Code 里可以直接让它使用：

```text
请使用 style-analyzer 帮我分析文风
请使用 copy-sop 帮我改这篇文案
请使用 wechat-publisher 帮我放进公众号草稿箱
```

### Install Only One Skill For Claude Code

只想用爆款文案 SOP：

```bash
mkdir -p ~/.claude/skills
cp -R copy-sop ~/.claude/skills/
```

只想分析文风：

```bash
mkdir -p ~/.claude/skills
cp -R style-analyzer ~/.claude/skills/
```

只想上传公众号草稿：

```bash
mkdir -p ~/.claude/skills
cp -R wechat-publisher ~/.claude/skills/
```

### Install For Codex / WorkBuddy / Other Coding Agents

如果你的工具支持本地 skills 目录，把对应文件夹复制进去即可。

常见位置可能是：

```text
~/.agents/skills/
<your-workspace>/.agents/skills/
```

例如装到 `~/.agents/skills/`：

```bash
mkdir -p ~/.agents/skills
cp -R style-analyzer ~/.agents/skills/
cp -R copy-sop ~/.agents/skills/
cp -R wechat-publisher ~/.agents/skills/
```

如果你的 agent 不能直接安装 skill，也可以把这个 GitHub 链接发给它，让它读取你要用的子文件夹：

```text
https://github.com/chestnutzoe/chestnut-copy-skill
```

并明确告诉它从哪个文件开始：

```text
请读取 copy-sop/SKILL.md，并按这个 skill 帮我写文案。
```

## Usage

### Use The Full Workflow

用 Claude Code plugin 安装后，可以这样调用：

```text
/chestnut:style-analyzer
/chestnut:copy-sop
/chestnut:wechat-publisher
```

完整工作流可以这样告诉 agent：

```text
请先用 /chestnut:style-analyzer 读取我的历史文案，生成文风说明；
再用 /chestnut:copy-sop 帮我写公众号母稿和封面标题 Hook；
最后用 /chestnut:wechat-publisher 帮我检查标题、摘要、封面，并放进公众号草稿箱。
```

完整流程会做：

1. 生成或刷新 `文风说明.md`
2. 用爆款文案 SOP 判断选题、结构、封面标题 Hook、留存率
3. 检查公众号 API 配置、IP 白名单、封面图
4. 只创建公众号草稿，不自动发布

### Use Only 文风分析

```text
请使用 style-analyzer，读取我的公众号历史文章或本地文案，生成一份文风说明。
```

如果用户没有公众号 API，也可以让它读取本地 Markdown、HTML、TXT 或 JSON 文件。

Claude Code plugin 调用方式：

```text
/chestnut:style-analyzer
```

### Use Only 爆款文案 SOP

```text
请使用 copy-sop，帮我判断这个选题值不值得写，并给我 3 组封面 / 标题 / Hook。
```

它可以单独用；如果已经有 `文风说明.md`，效果会更像用户本人。

Claude Code plugin 调用方式：

```text
/chestnut:copy-sop
```

### Use Only 公众号发布

```text
请使用 wechat-publisher，帮我把这篇本地 Markdown/HTML 文章放进公众号草稿箱。
```

Claude Code plugin 调用方式：

```text
/chestnut:wechat-publisher
```

在真正上传前，它应该先确认：

- 本地已有 `WECHAT_MP_APPID`
- 本地已有 `WECHAT_MP_APPSECRET`
- 当前公网 IP 已加入公众号后台 IP 白名单
- 用户已经确认要创建草稿
- 已有本地封面图或永久素材 `thumb_media_id`

## 公众号凭证

只有这两种情况需要公众号凭证：

- `style-analyzer/` 要从公众号后台读取历史文章；
- `wechat-publisher/` 要把文章上传到公众号草稿箱。

本地长期配置推荐创建一个不会进 Git 的密钥文件：

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

已存在的系统环境变量优先，不会被文件覆盖。

`.secrets/`、`.env`、`outputs/` 已写进 `.gitignore`。不要把 AppSecret、access token、下载文章 JSON、个人文风说明上传到 GitHub。

## 公众号发布前置检查

`wechat-publisher/` 在真正调用公众号 API 前，必须确认：

- 本地已经配置 `WECHAT_MP_APPID`
- 本地已经配置 `WECHAT_MP_APPSECRET`
- 当前机器公网 IP 已加入公众号后台 IP 白名单
- 用户已经确认要创建草稿
- 已有本地封面图或永久素材 `thumb_media_id`

如果用户本机还没配置公众号 API，AI 应该先提示用户创建 `.secrets/wechat-mp.env`，不要让用户把真实 AppSecret 发到聊天里。

## 封面规则

公众号草稿必须有封面。

发布 skill 创建真实草稿前，会先确认：

```text
你现在有公众号封面图吗？
如果有，请给我本地图片路径；
如果已经有永久素材 thumb_media_id，也可以直接给 media_id。
没有的话，我先给你封面方向 / AI 生成提示词，等你确认封面后再创建草稿。
```

没有封面时，只给封面方向或 AI 生成提示词，不创建真实草稿。

## 安全边界

- 默认只创建草稿，不自动发布。
- 不自动群发。
- 不自动定时发布。
- 真实 AppSecret 不写进聊天记录、Skill 文件、README 或 GitHub。
- 草稿创建后，必须去公众号后台人工检查排版、图片、标题、摘要和错别字，再手动发布。

## 常见问题

### 我应该安装哪一个？

如果用 Claude Code，推荐直接安装完整 `chestnut` plugin：

```text
/plugin marketplace add https://github.com/chestnutzoe/chestnut-copy-skill
/plugin install chestnut@chestnut
```

安装后按需要调用：

```text
/chestnut:style-analyzer
/chestnut:copy-sop
/chestnut:wechat-publisher
```

如果你的工具只支持手动复制 skill 文件夹，也可以只复制你需要的子文件夹。

### 我只想用爆款文案 SOP，可以吗？

可以。Claude Code plugin 安装后直接用：

```text
/chestnut:copy-sop
```

手动安装时，只复制：

```text
copy-sop/
```

### 我想先生成自己的文风，再写文案，怎么用？

Claude Code plugin 安装后，先运行：

```text
/chestnut:style-analyzer
```

生成 `文风说明.md` 后，再运行：

```text
/chestnut:copy-sop
```

手动安装时，复制：

```text
style-analyzer/
copy-sop/
```

### 没有公众号 API，可以用吗？

可以。`style-analyzer` 支持读取本地 Markdown、HTML、TXT 或 JSON 文案文件；`copy-sop` 完全不需要公众号 API。

只有这两种情况需要公众号 API：

- 从公众号后台读取历史文章
- 把文章上传到公众号草稿箱

### 我想把文章放进公众号草稿箱，需要准备什么？

需要准备：

```text
style-analyzer/
wechat-publisher/
```

或者 Claude Code plugin 安装后运行：

```text
/chestnut:wechat-publisher
```

正式上传前，还需要：

- 本地配置 `WECHAT_MP_APPID`
- 本地配置 `WECHAT_MP_APPSECRET`
- 当前公网 IP 已加入公众号后台 IP 白名单
- 准备好本地封面图，或已有永久素材 `thumb_media_id`
- 确认只创建草稿，不自动发布

### 这个会自动发布公众号吗？

不会。默认只创建草稿，不自动群发、不定时发布。草稿创建后，需要你自己去公众号后台人工检查并发布。

### 我的 AppSecret 或文风说明会被上传到 GitHub 吗？

不会自动上传。这个 repo 已经把这些路径写进 `.gitignore`：

```text
.env
.env.*
.secrets/
outputs/
articles.json
文风说明.md
```

不要把真实 AppSecret 发到聊天里，也不要手动提交到 GitHub。

### Codex、WorkBuddy、其他 agent 能用吗？

可以。把 GitHub 链接发给 agent，并告诉它读取对应的 `SKILL.md`：

```text
https://github.com/chestnutzoe/chestnut-copy-skill
请读取 copy-sop/SKILL.md，并按这个 skill 帮我写文案。
```
