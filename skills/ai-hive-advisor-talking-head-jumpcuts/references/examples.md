# 口播跳剪顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：保留最佳重述

```text
这段同一句说了三次，帮我选一次留下，保留完整意思并标剪点。
```

预期交付：有原片依据的删留表及选择理由。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-talking-head-jumpcuts",
  "request": "这段同一句说了三次，帮我选一次留下，保留完整意思并标剪点。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：自然停顿

```text
这条口播只删口误和明显重复，正常思考停顿尽量保留，不加音乐。
```

预期交付：符合保留条件的跳剪建议与接点核验。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-talking-head-jumpcuts",
  "request": "这条口播只删口误和明显重复，正常思考停顿尽量保留，不加音乐。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
