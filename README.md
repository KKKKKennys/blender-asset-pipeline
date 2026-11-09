<p align="center"><img src="assets/cover.svg" alt="Blender Asset Pipeline V2"></p>

# Blender Asset Pipeline · V2

**把模型命名、材质检查和导出步骤整理成可复用的 Skill。**

`V2.0.0` · `Blender` · `Agent Skill` · `Python 3.8+ checks` · `MIT`

[复制安装指令](#安装发给-agent-即可) · [实际怎么用](#从一句需求开始) · [使用规则与边界](#使用规则与边界) · [完整规则](SKILL.md) · [版本记录](CHANGELOG.md)

面向三维美术与 Agent 协作的资产整理 Skill，由 **李铿 / Kenny** 维护。我确定需要整理的模型和交付要求，Agent 按规则检查名称、材质与贴图，再执行获准的整理和导出任务。每项结果分别记录，方便继续修改。

<img src="assets/workflow.svg" alt="确定范围、检查计划、处理副本、导出回读的四阶段流程">

## 安装：发给 Agent 即可

点击下面代码块右上角的复制按钮，把整段发给支持本地 Skills 的 Agent。第一次用不需要自己找文件夹。

```text
请安装 Blender Asset Pipeline v2.0.0：
https://github.com/KKKKKennys/blender-asset-pipeline
先阅读 INSTALL.md，安装到当前 Agent 的用户技能目录；已有同名版本先备份再升级。
完成后告诉我版本、路径和调用方式，仅安装，不操作工程。
```

**只想复制一个链接？** 把这个链接发给 Agent，并说“帮我按页面安装”：

```text
https://raw.githubusercontent.com/KKKKKennys/blender-asset-pipeline/main/INSTALL.md
```

[查看详细安装与回退方法](INSTALL.md)。Codex、Claude Code 可使用各自的技能目录；安装 Skill 不会自动安装 Blender 或连接 MCP。

## 它解决什么

| 你遇到的事 | Skill 会怎样组织工作 | 可交付的结果 |
|---|---|---|
| 一批对象需要统一名字 | 按对象身份先做映射，检查命名空间和已有名称 | 原名 → 新名清单、冲突与跳过项 |
| 贴图看起来缺了 | 区分外部文件、打包图、UDIM、序列与节点组 | 带对象和槽位的问题定位 |
| 需要逐项交付 GLB / FBX | 明确根对象与依赖、输出位置及覆盖策略 | 逐资产导出清单 |
| 文件导出了但不知道能否用 | 把生成、重新导入、外观检查分开记录 | 有证据范围的交付报告 |
| 中途失败，重新跑怕重复修改 | 对照计划指纹与已完成动作，只重试失败项 | 可追溯的恢复说明 |

## 从一句需求开始

### 01 · 只检查

```text
使用 $blender-asset-pipeline 检查当前选择的道具。
只报告重名、空材质槽与缺失贴图，保持工程原样。
```

### 02 · 整理一个明确范围

```text
使用 $blender-asset-pipeline 整理 Props 集合，在副本中执行。
按我提供的命名表处理，保留共享网格与材质，输出改名对照和跳过原因。
```

### 03 · 导出并核对

```text
使用 $blender-asset-pipeline 将这些资产分别导出为 GLB。
保留层级，输出到我指定的目录；已有同名文件不要覆盖。
回读核对尺寸、材质分配与贴图，把未验证项单列。
```

更完整的输入与输出约定见 [调用示例](examples/requests.md)。格式、引擎和命名规则由任务决定。

## V2 更新

| V1 已有 | V2 增加 |
|---|---|
| 检查 / 整理 / 导出的任务分流 | 明确计划版本、范围 ID、执行状态与恢复规则 |
| 重名和共享数据的说明 | 可运行的只读计划检查器，验证交换改名、跨命名空间与越界动作 |
| 逐项导出与回读要求 | 输出路径碰撞、大小写差异、已有文件覆盖的计划检查 |
| 基础报告模板 | 每项独立的生成 / 回读 / 外观状态，不用一个“通过”覆盖失败 |
| 手动下载 | 固定版本安装说明、备份升级与回退入口 |

这里的检查器只分析 JSON 计划，不会执行 Blender 操作，也不能验证实际网格、材质或许可。

## 使用规则与边界

- 先确定要处理哪些模型；“只检查”任务只输出问题清单。
- 改名前保留对照表；共享网格、材质和外部链接分别处理。
- 导出、重新导入和外观检查分别记录，失败与待确认项单独列出。

附带的 Python 检查器只检查 JSON 计划，不会连接 Blender 或修改模型。具体检查规则及合成用例保留在[设计说明](docs/design-notes.md)，实际资产仍需在软件中核对。

[检查器修订 PR #1](https://github.com/KKKKKennys/blender-asset-pipeline/pull/1) 在 2026-11-09 核对时仍为草稿、未合并；其中的修复与测试记录不代表当前主分支已包含该修复。

## 可运行的计划检查

在下载的仓库根目录运行：

```bash
python scripts/check_plan.py examples/organize-export-plan.json
python -m unittest discover -s tests -v
```

命令返回 `valid: true` 只代表计划内部一致。它不会连接 Blender，也不能代替现场检查。JSON 字段见 [V2 执行约定](references/execution-v2.md)。

## 文件导航

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | Agent 入口与按需阅读路线 |
| [规则参考](references/rules.md) | 材质、贴图、共享数据和导出边界 |
| [V2 执行约定](references/execution-v2.md) | 范围、计划、执行、恢复及验证 |
| [交付记录](references/delivery-record.md) | 逐资产状态和报告模板 |
| [示例计划](examples/organize-export-plan.json) | 虚构输入，可用于检查器练习 |
| [制作复盘](docs/design-notes.md) | 为什么改、改了什么、验证到哪一步 |

<details><summary><b>常见问题</b></summary>

**会自动改整个场景吗？** 不会。任务必须有明确的选择、集合或根对象范围。

**安装后就能控制 Blender 吗？** 还需要可用的 Blender MCP 或用户指定的 Blender Python 环境。检查器本身只用 Python 标准库。

**支持生成模型吗？** 此 Skill 整理已有资产，不负责新建模型或重设计材质。

**能保证所有材质导出后一模一样吗？** 不能。程序纹理、节点与目标格式存在差异，需要单独决定是否烘焙并做外观检查。

**能写效率提升百分比吗？** 当前没有生产批次基准。应先在真实任务测量，不能从规则条数推导效率数字。
</details>

---
作者与维护：**李铿 / Kenny** · [MIT License](LICENSE) · [发布版本](https://github.com/KKKKKennys/blender-asset-pipeline/releases)

Instruction-led Blender asset delivery, with a local preflight checker. No Blender add-on or production asset bundle included.
