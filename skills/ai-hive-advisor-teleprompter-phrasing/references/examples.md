# 提词器断句顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：手机提词

```text
把这份500字稿排成手机提词版，数字连同单位保留，短停用斜线标记。
```

预期交付：语义完整的提词稿、标记说明和实读校准建议。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-teleprompter-phrasing",
  "request": "把这份500字稿排成手机提词版，数字连同单位保留，短停用斜线标记。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：容易抢字

```text
我用两分钟读完这段稿，但遇到长句总追不上，帮我改断句，不改内容。
```

预期交付：长句语义分段和按本人实读调整的设置建议。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-teleprompter-phrasing",
  "request": "我用两分钟读完这段稿，但遇到长句总追不上，帮我改断句，不改内容。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
