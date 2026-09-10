# 视频画质修复顾问：具体场景示例

以下是给 Agent 的任务参考，不是可直接提交到 AI-HIVE 的 API 参数。示例不自动授权付费制作或外部发布。

## 场景 1：导出变糊

```text
原片比导出清楚，先比较这两个文件，不要直接做AI增强。
```

预期交付：损失阶段判断与重导出优先方案。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-video-quality-repair",
  "request": "原片比导出清楚，先比较这两个文件，不要直接做AI增强。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 场景 2：低光噪点

```text
这段店内视频偏暗有噪点，只拿10秒试修，商品标签不能被改字。
```

预期交付：有限小样方案、标签保真和副作用核验。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-advisor-video-quality-repair",
  "request": "这段店内视频偏暗有噪点，只拿10秒试修，商品标签不能被改字。",
  "external_actions": "未授权，不执行发布、群发或投放",
  "paid_generation": "未授权，先给方案与预算"
}
```

## 需要生成素材时

按 [MCP 绑定说明](mcp-binding.md) 查询实际工具、模型与参数，用户批准数量和预算后，再按单次调用代码提交并复用任务 ID 查询结果。纯诊断不执行生成步骤。
