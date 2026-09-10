# 视频信息密度顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：概念过多

```text
这段60秒脚本有八个概念，新手看不懂，允许拆成两条但别删安全提醒。
```

预期交付：概念依赖、两条结构与保留提醒核对。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-information-density",
  "request": "这段60秒脚本有八个概念，新手看不懂，允许拆成两条但别删安全提醒。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：画面文字过载

```text
画面上有三组数据，旁白也在讲新观点，帮我安排先后呈现。
```

预期交付：按理解顺序安排的画面与旁白分工。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-information-density",
  "request": "画面上有三组数据，旁白也在讲新观点，帮我安排先后呈现。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
