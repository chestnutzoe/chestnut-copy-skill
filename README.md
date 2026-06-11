# Chestnut Copy Skill Set

这是 Zoe / Chestnut 的中文创作者文案 Skill 套装。

它不是一个单独 Skill，而是三个可以独立安装、也可以组合使用的 Skill：

| Skill | 中文名 | 负责什么 | 可以单独用吗 |
| --- | --- | --- | --- |
| `chestnut-style-analyzer` | 文风分析 | 从公众号历史文章或本地文案里总结个人文风，生成 `文风说明.md` | 可以 |
| `chestnut-copy-sop` | Chestnut 爆款文案 SOP | 用 Zoe/Chestnut 的方法做选题、洞察、结构、封面标题 Hook、留存率和去 AI 味 | 可以 |
| `wechat-draft-assistant` | 公众号发布助手 | 处理标题、摘要、封面预检，并把确认后的文章上传到公众号草稿箱 | 可以 |

## 推荐使用方式

完整流程：

```text
文风分析 -> Chestnut 爆款文案 SOP -> 公众号发布助手
```

三层分工：

1. **文风分析**
   负责“像不像你”。推荐读取公众号历史母稿，也支持本地 Markdown、HTML、TXT、JSON 文案。

2. **Chestnut 爆款文案 SOP**
   负责“有没有传播力”。重点是选题判断、用户洞察、痛点、结构、封面标题 Hook、人味注入、去 AI 味、留存率检查。

3. **公众号发布助手**
   负责“怎么落地”。重点是标题、摘要、封面、公众号草稿箱、发布前人工审核。

## 文件结构

```text
.
├── README.md
├── chestnut-style-analyzer/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/wechat-api.md
│   └── scripts/fetch_wechat_articles.py
├── chestnut-copy-sop/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/chestnut-copy-sop.md
└── wechat-draft-assistant/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/wechat-api.md
    └── scripts/publish_draft.py
```

## 怎么安装

### 只装一个

只复制你需要的那个文件夹到 AI 工具的 skills 目录。

比如只想用爆款文案方法：

```text
chestnut-copy-sop/
```

### 三个一起装

把这三个文件夹都复制到 skills 目录：

```text
chestnut-style-analyzer/
chestnut-copy-sop/
wechat-draft-assistant/
```

文件夹名用英文，是为了兼容 Claude Code、Codex、WorkBuddy 等工具；用户看到的名字在 `agents/openai.yaml` 里是中文。

## 公众号凭证

只有这两种情况需要公众号凭证：

- `文风分析` 要从公众号后台读取历史文章；
- `公众号发布助手` 要把文章上传到公众号草稿箱。

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

## 封面规则

公众号草稿必须有封面。

发布助手创建真实草稿前，会先确认：

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

### 我只想让别人用 Chestnut 爆款文案 SOP，必须装三个吗？

不用。只安装 `chestnut-copy-sop/` 就可以。

### 我想让别人读取自己的文风后再写文案，怎么装？

安装：

```text
chestnut-style-analyzer/
chestnut-copy-sop/
```

先生成 `文风说明.md`，再让 `Chestnut 爆款文案 SOP` 读取这份文风。

### 我想把文章放到公众号草稿箱，怎么装？

安装：

```text
wechat-draft-assistant/
```

如果还需要读取公众号历史文章生成文风，再加：

```text
chestnut-style-analyzer/
```
