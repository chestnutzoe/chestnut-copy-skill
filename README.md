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
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── style-analyzer/
│   ├── Chestnut-cop/
│   └── wechat-publiser/
├── LICENSE
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

### Via Claude Code Custom Marketplace Source

Install directly from this public GitHub repo. Run these as separate Claude Code messages; do not paste all lines into the prompt at once.

First add this repository as a marketplace source:

```text
/plugin marketplace add https://github.com/chestnutzoe/chestnut-copy-skill
```

Then install whichever skill you want.

Install **文风分析**:

```text
/plugin install chestnut-copy-skill@style-analyzer
```

Install **爆款文案 SOP**:

```text
/plugin install chestnut-copy-skill@Chestnut-cop
```

Install **公众号发布**:

```text
/plugin install chestnut-copy-skill@wechat-publiser
```

If you want the full workflow, run all three install commands one by one.

Use the HTTPS URL. The shorter `chestnutzoe/chestnut-copy-skill` form may make Claude Code try SSH, which can fail if GitHub is not already in your `known_hosts` file.

After plugin installation, Claude Code namespaces skills as:

```text
/plugin-name:skill-name
```

For example:

```text
/style-analyzer:style-analyzer
/Chestnut-cop:Chestnut-cop
/wechat-publiser:wechat-publiser
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

这个仓库目前是 **3 个独立 Skill 的套装**，不是单个根目录 Skill。真正的 skill 文件夹是：

```text
style-analyzer/
Chestnut-cop/
wechat-publiser/
```

每个文件夹都可以单独复制到你的 AI 工具 skills 目录里。

### Fast Install For Claude Code

如果你想一次装完三个 skill，可以直接运行：

```bash
git clone https://github.com/chestnutzoe/chestnut-copy-skill.git /tmp/chestnut-copy-skill
mkdir -p ~/.claude/skills
cp -R /tmp/chestnut-copy-skill/style-analyzer ~/.claude/skills/
cp -R /tmp/chestnut-copy-skill/Chestnut-cop ~/.claude/skills/
cp -R /tmp/chestnut-copy-skill/wechat-publiser ~/.claude/skills/
```

如果你之后重新下载，先删除 `/tmp/chestnut-copy-skill` 或换一个临时目录。

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

## Usage

### Use The Full Workflow

装了三个 skill 后，可以这样告诉 agent：

```text
请先用 style-analyzer 读取我的历史文案，生成文风说明；
再用 Chestnut-cop 帮我写公众号母稿和封面标题 Hook；
最后用 wechat-publiser 帮我检查标题、摘要、封面，并放进公众号草稿箱。
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

### Use Only 爆款文案 SOP

```text
请使用 Chestnut-cop，帮我判断这个选题值不值得写，并给我 3 组封面 / 标题 / Hook。
```

它可以单独用；如果已经有 `文风说明.md`，效果会更像用户本人。

### Use Only 公众号发布

```text
请使用 wechat-publiser，帮我把这篇本地 Markdown/HTML 文章放进公众号草稿箱。
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
