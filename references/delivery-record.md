# V2 交付记录

以下是空模板，不是执行结果。`rules_version` 记录技能版本，`schema_version` 记录报告结构。

```json
{
  "schema_version": "2.0",
  "rules_version": "2.0.0",
  "mode": "audit",
  "scope": {"blend_file": null, "asset_roots": []},
  "software_version": null,
  "findings": [],
  "actions": [],
  "exports": [],
  "errors": []
}
```

问题：`rule_id / severity / object_id / observed / suggested_action / evidence`。
动作：`id / object_id / old / new / state / error`，state 使用 `planned / done / failed / skipped`。
导出：`object_id / relative_path / format / settings / bytes / generated / reimport / visual`。

三个检查字段都使用 `{status, evidence}`；status 为 `not_run / passed / failed / blocked`。例如已生成但尚未回读的文件必须写 `generated: passed`、`reimport: not_run`、`visual: not_run`，不能汇总成全部合格。

汇总表可以简化为：资产 | 名称修改 | 贴图问题 | 文件 | 回读 | 外观。生产执行时填写实际值；仅设计时用空值或明确“示例”。公开报告使用相对路径，不含客户资产、凭据或本机工作目录。
