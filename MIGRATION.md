# Skill 更名为 chestnut-copy（2.3.1）

Skill 正式名称为 `chestnut-copy`，显示名称为 **Chestnut Copy**。原来的 `chestnut-copy-sop` 名称停止使用。仓库地址 `chestnut-copy-skill` 保持不变，兼容整包插件身份 `chestnut@chestnut` 也保留，但其中只有一个 `chestnut-copy` Skill。

- 手动安装：下载新版 `chestnut-copy.zip`，先备份旧文件夹中的个人修改，再将旧 `chestnut-copy-sop` 文件夹替换为 `chestnut-copy`，避免重复加载。
- 使用 `chestnut@chestnut` 插件：更新后新开会话，调用 `/chestnut:chestnut-copy`。
- 原来单独安装 `chestnut-copy-sop@chestnut` 插件：通过客户端卸载旧入口，改装 `chestnut-copy@chestnut`。下载/更新不会自动修改手动安装副本。

## 之前的拆分：Copy 2.3.0

Copy 仓库现在只包含 `chestnut-copy`。原仓库地址与 `chestnut@chestnut` 插件身份保留。

版本变化：2.2.0 曾包含七个工具；2.2.1 恢复三个文案相关工具；2.3.0 进一步将文风分析和公众号发布独立出去，Copy 只负责文案。

## 根据安装方式处理

- **ZIP / 手动复制：** 本地文件不会自动变化。需要新版 Copy 时，下载单项 ZIP 替换对应文件夹，先保留自己的修改。其他已装工具可以继续独立使用，无需为了更新 Copy 而删除它们。
- **旧整包插件：** 更新原来的 marketplace 和 `chestnut` 插件，然后新开会话检查加载列表。新版插件只含 Copy。如果仍显示其他工具，检查手动安装副本或客户端缓存；必要时通过客户端卸载并重新安装 Copy 插件。各客户端的缓存移除行为未逐一实测。
- **从旧 marketplace 单独安装过文风分析、公众号发布或品牌工具：** 这些入口已移出旧目录。公众号发布已停止分发；其他仍提供的工具需要继续使用时，从新工具箱下载对应完整单项，保留本地修改，再通过客户端卸载旧的对应插件，避免重复。新工具箱不会自动迁移安装记录。

独立下载：

- [文风分析 ZIP](https://github.com/chestnutzoe/chestnut-skills/releases/latest/download/chestnut-style-analyzer.zip)
- [其他工具与完整工具箱](https://github.com/chestnutzoe/chestnut-skills)

文风分析继续提供独立下载。公众号发布 Skill 已从当前工具箱移除，其独立仓库保留并归档；旧版本安装在本地的副本不会自动删除，可通过客户端卸载。
