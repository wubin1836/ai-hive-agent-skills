# 系列视频编排顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：五集入门

```text
把这些选题排成五集手机拍摄入门，每集独立看也能学会一点。
```

预期交付：五集职责、前提和单集验收目标。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-series-sequence",
  "request": "把这些选题排成五集手机拍摄入门，每集独立看也能学会一点。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：重复修整

```text
这六条脚本反复讲同一个概念，帮我调整次序和分工，不加集数。
```

预期交付：去重后的分集地图与必要回顾位置。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-series-sequence",
  "request": "这六条脚本反复讲同一个概念，帮我调整次序和分工，不加集数。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
