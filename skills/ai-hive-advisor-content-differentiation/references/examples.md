# 同质化内容诊断顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：同行雷同

```text
这三条我的脚本和两条公开对照讲法很像，找能用真实经历改出差异的地方。
```

预期交付：重复依据、真实差异资源和可执行改写方向。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-content-differentiation",
  "request": "这三条我的脚本和两条公开对照讲法很像，找能用真实经历改出差异的地方。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：同题不同证据

```text
大家都在讲办公室收纳，我有一次真实搬迁记录，帮我找一个可验证的新角度。
```

预期交付：由搬迁材料支撑的不同问题与证据设计。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-content-differentiation",
  "request": "大家都在讲办公室收纳，我有一次真实搬迁记录，帮我找一个可验证的新角度。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
