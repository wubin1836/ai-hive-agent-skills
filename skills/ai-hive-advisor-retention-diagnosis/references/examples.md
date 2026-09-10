# 视频完播诊断顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：中途掉点

```text
这条80秒视频在25秒附近掉得快，结合曲线和成片给两个可验证假设。
```

预期交付：时间轴对应、假设依据和两项修改测试。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-retention-diagnosis",
  "request": "这条80秒视频在25秒附近掉得快，结合曲线和成片给两个可验证假设。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：不同片长比较

```text
两条视频分别30秒和90秒，别只按完播率判断，帮我检查口径。
```

预期交付：可比指标说明与数据能支持的有限结论。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-retention-diagnosis",
  "request": "两条视频分别30秒和90秒，别只按完播率判断，帮我检查口径。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
