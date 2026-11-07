# 交给 Agent 安装 · Blender Asset Pipeline V2

当前稳定版本：`v2.0.0`。技能目录名：`blender-asset-pipeline`。

## 复制这段到 Agent 聊天框

```text
请安装这个 Agent Skill 的 v2.0.0 版本：
https://github.com/KKKKKennys/blender-asset-pipeline
先阅读仓库 INSTALL.md，再安装到当前 Agent 支持的用户技能目录。
如果已有同名版本，先备份再升级；保留我的其他技能和配置。
完成后报告安装路径、版本及如何调用。仅安装，不操作我的工程。
```

也可以只发送本页链接，并说明“按这个页面帮我安装 Skill”：

```text
https://raw.githubusercontent.com/KKKKKennys/blender-asset-pipeline/main/INSTALL.md
```

## Agent 的安装步骤

1. 确认当前 Agent、操作系统和实际技能目录。Codex 通常是 `~/.codex/skills/`，Claude Code 通常是 `~/.claude/skills/`；用户配置了其他目录时优先使用配置。未知 Agent 先查它的本地文档，不能宣称任意聊天产品都支持安装。
2. 优先使用当前 Agent 自带的 Skill 安装器，指定仓库 `KKKKKennys/blender-asset-pipeline`、仓库根目录、ref `v2.0.0`、安装名 `blender-asset-pipeline`。没有安装器时，把该 tag 克隆/下载到独立临时目录，不在现有技能目录上直接 clone 覆盖。
3. 核对 `VERSION` 为 `2.0.0`，根目录有 `SKILL.md`，所有被引用的脚本、参考与资源都存在。完整复制技能包；不要只下载一个 `SKILL.md`，也不要把 `.git` 或测试缓存放进安装目录。
4. 如果目标已存在，保留整目录备份。用户对安装本版本的要求包含此次升级，但不允许合并掉其本地自定义规则；有自定义内容时说明差异并保留可回退副本。只替换本技能。
5. 检查目标目录及入口可读。列出安装位置与版本；需要时让用户新开一次会话以重新发现技能。安装成功不代表 Blender / MCP 或 Remotion 依赖也已就绪。

## 无需运行的东西

安装不执行模型处理、相机动画、渲染或项目脚本，不安装 Blender，也不修改全局代理或其他 Agent 设置。包内检查工具使用 Python 3.8+ 标准库，可在需要时单独运行。

## 升级与回退

从 V1 升级时目录名保持不变；在 README 的“V2 更新”查看变化。要回退可恢复安装前备份，或安装仓库 `v1.0.0` tag。正在执行的项目继续依据它记录的规则版本，不在任务中途静默切换。

若下载因网络失败，报告失败步骤，保持原安装完整；不要把不完整下载当作安装成功。
