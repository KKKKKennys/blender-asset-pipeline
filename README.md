<p align="center"><img src="assets/cover.svg" alt="Blender Asset Pipeline V2"></p>

# Blender Asset Pipeline · V2

**从“帮我整理这些资产”，到范围清楚、修改可追踪、结果可核对的交付。**

`V2.0.0` · `Blender` · `Agent Skill` · `Python 3.8+ checks` · `MIT`

[复制安装指令](#安装发给-agent-即可) · [实际怎么用](#从一句需求开始) · [制作问题与迭代](#为什么做第二版) · [完整规则](SKILL.md) · [版本记录](CHANGELOG.md)

面向三维美术与 AI 协作的资产准备流程，由 **李铿 / Kenny** 维护。适合现有场景中的道具整理、材质检查和按资产交付。Agent 负责理解规范与调用软件，Skill 提供操作边界和检查方法。

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

## 为什么做第二版

制作首版时，把“先检查、再执行”写进说明还不够：Agent 仍需要知道**检查什么、什么时候算完成、失败后从哪里继续**。

| 设计中需要解决的问题 | V2 的处理 | 如何核验 |
|---|---|---|
| A 与 B 互换名称，被当成普通重名 | 计划允许完整名称置换；执行时使用临时唯一名 | 合成计划测试，不冒充 Blender 实测 |
| 对象和材质叫同一个名字，被错误合并 | 各命名空间独立判断 | 计划检查用例 |
| `Chair.glb` / `chair.glb` 在交付目录碰撞 | 默认按不区分大小写的目标路径检查，可按平台配置 | 计划检查用例 |
| 只想导出，却顺手改名 | `export` 模式拒绝改名动作 | 模式边界用例 |
| 一个文件失败，汇总仍写“全部完成” | 每个资产保留失败和未执行状态 | 报告模板与执行记录要求 |

上述是本次规则设计与合成数据验证，不声称已在生产工程中发生或解决全部情形。[阅读完整设计复盘](docs/design-notes.md)

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
