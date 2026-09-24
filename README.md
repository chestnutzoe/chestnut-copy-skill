# Chestnut Copy · 文案 Skill

**Copy 就是 Copy。** 这个仓库只提供 `chestnut-copy`：判断选题、写标题与 Hook、创作正文、诊断逐字稿和精准改稿。

原仓库地址和 `chestnut@chestnut` 插件身份保留。2.3.1 的 Skill 名称为 `chestnut-copy`，插件只加载一个文案 Skill；文风分析、公众号发布和其他工具均独立分发。

## 下载与使用

- [查看文案 Skill](chestnut-copy/SKILL.md)
- [只下载 Copy Skill ZIP](https://github.com/chestnutzoe/chestnut-copy-skill/releases/latest/download/chestnut-copy.zip)
- [其他独立 Skills 与全套下载](https://github.com/chestnutzoe/chestnut-skills)

解压单项 ZIP，将 `chestnut-copy` 文件夹放入所用 AI 工具的 skills 目录。保留里面的 `references/`，不要只复制 SKILL.md。

你可以直接说：

```text
请使用 chestnut-copy 帮我判断这个选题，并写出标题、Hook 和正文。
请使用 chestnut-copy 诊断这篇逐字稿，保留有效内容，精准改稿。
```

已有 `文风说明.md` 时会读取；没有也能独立完成文案。这个 Skill 不需要公众号 API，也不会上传或发布文章。

## Claude Code 插件安装

先添加来源，再安装（分两次执行）：

```text
/plugin marketplace add https://github.com/chestnutzoe/chestnut-copy-skill
```

```text
/plugin install chestnut@chestnut
```

使用 `/chestnut:chestnut-copy`。原有用户继续更新这个插件即可。

## Codex 插件安装

```bash
codex plugin marketplace add chestnutzoe/chestnut-copy-skill
codex plugin add chestnut@chestnut
```

安装后新建任务加载 Skill。Marketplace 里保留 `chestnut-copy` 单项插件入口以兼容已有安装；两个入口都只含同一个 Copy Skill，任选其一，不必重复安装。

## 文风分析和公众号发布在哪里？

它们现在各自独立，不再随 Copy 安装：

- [文风分析](https://github.com/chestnutzoe/chestnut-skills/tree/main/skills/chestnut-style-analyzer) · [单独下载](https://github.com/chestnutzoe/chestnut-skills/releases/latest/download/chestnut-style-analyzer.zip)
- [公众号草稿发布](https://github.com/chestnutzoe/chestnut-skills/tree/main/skills/chestnut-wechat-publisher) · [单独下载](https://github.com/chestnutzoe/chestnut-skills/releases/latest/download/chestnut-wechat-publisher.zip)

已经安装过旧版组合包，请看 [迁移说明](MIGRATION.md)。

## 维护范围

`chestnut-copy/` 是本仓库文案内容的维护源；两个插件入口是兼容安装用的发行副本，内容须保持一致。新增独立 Skill 不加入本仓库。私人 Chestnut Skills 不同步到公开包。
