# 从 2.2.0 混合版回到 Copy 工具包

2.2.0 曾把四个独立品牌工具加入 Copy 仓库。2.2.1 恢复三个文案工具，原地址与插件身份不变；文案工具内容保留。

## 根据安装方式处理

- **下载 ZIP / 手动复制：** 你的本地文件不会自动变化。若只安装过原来的三个文案工具，无需迁移。若装过七个且只想保留 Copy，请在自己的 skills 目录中移走以下四个对应文件夹。移动前保留个人修改；不要删除其他文件夹。
- **安装旧整包插件：** 在客户端更新原来的 marketplace 与 `chestnut` 插件，然后重新打开会话，查看实际加载的 Skills。2.2.1 包内只有下列三个文案工具。如果四个品牌工具仍出现，检查是否还存在手动安装副本或独立插件；必要时通过客户端卸载并重新安装旧 Copy 插件。不同客户端的缓存清理行为未逐一实测，不能保证一次更新会自动移除所有旧副本。
- **从旧 marketplace 单独安装过新增品牌插件：** 这些入口已从旧目录撤出。如需继续使用，先从新工具箱下载对应单项，再通过客户端卸载旧的对应插件，避免重复。新地址提供 Skills 文件，不会自动迁移你的插件安装记录。

保留的三个工具：

- `chestnut-copy-sop`
- `chestnut-style-analyzer`
- `chestnut-wechat-publisher`

迁到新入口的四个工具：

- `chestnut-brand-story`
- `chestnut-positioning-statement`
- `chestnut-brand-guidance`
- `chestnut-product-brief`

[新工具箱与单项下载](https://github.com/chestnutzoe/chestnut-skills) · [整包 ZIP](https://github.com/chestnutzoe/chestnut-skills/releases/latest/download/chestnut-skills.zip)

已经在用 Copy 的用户，只下载缺少的四个品牌工具即可，不需要重复安装三个文案工具。
