# Chestnut Copy

独立 Skill：`chestnut-copy`。本仓库可以单独下载、提 Issue、点 Star。

- [读取 Skill](SKILL.md)
- [下载完整 Skill ZIP](https://github.com/chestnutzoe/chestnut-copy-skill/releases/latest/download/chestnut-copy.zip)
- [全部 Chestnut Skills 与整包下载](https://github.com/chestnutzoe/chestnut-skills)

把 Skill 链接交给能读取 GitHub 的 AI，并说明要完成什么；需要安装时，下载完整 ZIP，解压后把 `chestnut-copy` 文件夹放入所用工具的 skills 目录，保留参考资料与脚本。

## 唯一维护源

内容在 [总仓库的 skills/chestnut-copy](https://github.com/chestnutzoe/chestnut-skills/tree/main/skills/chestnut-copy) 修改。本仓库由 GitHub Actions 自动发布，不手动维护第二份。修订请提交到总仓库；这里的 Issue 可以用来反馈此 Skill 的问题。

本次来源：[提交 7682c1bb52b2](https://github.com/chestnutzoe/chestnut-skills/commit/7682c1bb52b2232ef8bc8a6cb4d6709a03609d08)。对应文件清单见 [source.json](source.json)。

## 旧用户兼容

原仓库地址、`chestnut@chestnut` 插件身份及 Copy 文件夹链接保留。更新后调用 `/chestnut:chestnut-copy`。独立插件入口 `chestnut-copy@chestnut` 同样保留，两者只安装一个。

Claude Code 首次安装：

```text
/plugin marketplace add https://github.com/chestnutzoe/chestnut-copy-skill
/plugin install chestnut@chestnut
```

Codex 首次安装：

```text
codex plugin marketplace add chestnutzoe/chestnut-copy-skill
codex plugin add chestnut@chestnut
```

旧名称与组合包迁移见 [MIGRATION.md](MIGRATION.md)。Copy 只负责文案。
