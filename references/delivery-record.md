# 交付记录

下面是字段约定与空模板，不是已完成的执行报告。可按任务简化，避免输出无用日志。

```json
{
  "task": "asset-preflight",
  "mode": "audit",
  "scope": {"blend_file": null, "asset_roots": []},
  "software_version": null,
  "rules_version": "1.0",
  "findings": [],
  "rename_map": [],
  "exports": [],
  "verification": {"files_checked": false, "reimport_checked": false, "visual_checked": false},
  "skipped": [],
  "errors": []
}
```

单条问题包含 `rule_id / severity / object_path / observed / suggested_action / status`。
单条改名记录包含稳定对象标识、对象类型、旧名、新名、共享数据状态与实际执行结果。
单条导出记录包含资产根、格式、相对交付路径、大小、导出设置、验证状态。对失败导出给出原因，不填假路径。

可以附一张便于美术阅读的汇总表：`资产 | 命名 | 材质/贴图 | 导出 | 验证`。
在公开报告中使用项目相对路径；不发布本机用户名、完整工作目录、凭据或未授权客户资产。
