# Chestnut Copy Skill Set

这是 Zoe / Chestnut 的中文创作者文案 Skill 套装。

它不是一个单独 Skill，而是三个可以独立安装、也可以组合使用的 Skill：

| Skill 文件夹 | 中文名 | 负责什么 | 可以单独用吗 |
| --- | --- | --- | --- |
| `style-analyzer/` | 文风分析 | 从公众号历史文章或本地文案里总结个人文风，生成 `文风说明.md` | 可以 |
| `Chestnut-cop/` | 爆款文案 SOP | 用 Zoe/Chestnut 的方法做选题、洞察、结构、封面标题 Hook、留存率和去 AI 味 | 可以 |
| `wechat-publiser/` | 公众号发布 | 处理标题、摘要、封面预检、API/IP 前置检查，并把确认后的文章上传到公众号草稿箱 | 可以 |

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
├── README.md
├── style-analyzer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/wechat-api.md
│   └── scripts/fetch_wechat_articles.py
├── Chestnut-cop/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/chestnut-copy-sop.md
└── wechat-publiser/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/wechat-api.md
    └── scripts/publish_draft.py
```

## Installation

### Download This Repo

你可以用两种方式拿到文件：

1. GitHub 页面点击 **Code -> Download ZIP**，解压后选择要安装的 skill 文件夹。
2. 用命令行 clone：

```bash
git clone https://github.com/chestnutzoe/chestnut-copy-skill.git
cd chestnut-copy-skill
```

这个仓库目前是 **3 个独立 Skill 的套装**，不是单个根目录 Skill。真正的 skill 文件夹是：

```text
style-analyzer/
Chestnut-cop/
wechat-publiser/
```

每个文件夹都可以单独复制到你的 AI 工具 skills 目录里。

### Install All Three For Claude Code

把三个 skill 都装到 Claude Code：

```bash
mkdir -p ~/.claude/skills
cp -R style-analyzer ~/.claude/skills/
cp -R Chestnut-cop ~/.claude/skills/
cp -R wechat-publiser ~/.claude/skills/
```

安装后，在 Claude Code 里可以直接让它使用：

```text
请使用 style-analyzer 帮我分析文风
请使用 Chestnut-cop 帮我改这篇文案
请使用 wechat-publiser 帮我放进公众号草稿箱
```

### Install Only One Skill For Claude Code

只想用爆款文案 SOP：

```bash
mkdir -p ~/.claude/skills
cp -R Chestnut-cop ~/.claude/skills/
```

只想分析文风：

```bash
mkdir -p ~/.claude/skills
cp -R style-analyzer ~/.claude/skills/
```

只想上传公众号草稿：

```bash
mkdir -p ~/.claude/skills
cp -R wechat-publiser ~/.claude/skills/
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
cp -R Chestnut-cop ~/.agents/skills/
cp -R wechat-publiser ~/.agents/skills/
```

如果你的 agent 不能直接安装 skill，也可以把这个 GitHub 链接发给它，让它读取你要用的子文件夹：

```text
https://github.com/chestnutzoe/chestnut-copy-skill
```

并明确告诉它从哪个文件开始：

```text
请读取 Chestnut-cop/SKILL.md，并按这个 skill 帮我写文案。
```

### About Claude Code Plugin Install

Zara 的 `frontend-slides` 是 Claude Code plugin 包装，所以可以用 `/plugin marketplace add ...` 安装。

这个仓库当前先提供通用 skill 文件夹，适合 Claude Code、Codex、WorkBuddy 和其他能读取本地文件的 coding agent。后面如果要做成 Claude Code plugin marketplace 形式，需要再补 `.claude-plugin/` 配置。

## 公众号凭证

只有这两种情况需要公众号凭证：

- `style-analyzer/` 要从公众号后台读取历史文章；
- `wechat-publiser/` 要把文章上传到公众号草稿箱。

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

`wechat-publiser/` 在真正调用公众号 API 前，必须确认：

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

### 为什么 GitHub 上不是一个 `SKILL.md`？

因为这是三个独立 Skill 的套装。根目录是说明书，每个子文件夹才是一个真正的 Skill。

### 我只想让别人用爆款文案 SOP，必须装三个吗？

不用。只安装 `Chestnut-cop/` 就可以。

### 我想让别人读取自己的文风后再写文案，怎么装？

安装：

```text
style-analyzer/
Chestnut-cop/
```

先生成 `文风说明.md`，再让 `Chestnut-cop/` 读取这份文风。

### 我想把文章放到公众号草稿箱，怎么装？

安装：

```text
wechat-publiser/
```

如果还需要读取公众号历史文章生成文风，再加：

```text
style-analyzer/
```
