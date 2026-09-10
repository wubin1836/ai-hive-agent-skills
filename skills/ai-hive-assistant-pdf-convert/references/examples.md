# PDF转换助手：具体任务示例

这些是可交给宿主 Agent 的任务请求，不是伪造的 AI-HIVE API。所有示例均需按当前用户范围执行；媒体生成需要另行明确数量和预算。

## 示例 1：PDF转可编辑稿

```text
把这份文字版PDF转成Word，优先保留表格能编辑，页码变化可以接受。
```

期望交付：可编辑工作稿与表格核验结果，说明无法保留的布局。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-assistant-pdf-convert",
  "request": "把这份文字版PDF转成Word，优先保留表格能编辑，页码变化可以接受。",
  "external_actions": "未授权，不执行发布/投递/群发",
  "media_budget": "未授权，先给方案或询问预算"
}
```

## 示例 2：Word交付PDF

```text
把这份Word转成PDF供客户打印，确认页码和图表都完整。
```

期望交付：可打印PDF与分页、图表完整性检查。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-assistant-pdf-convert",
  "request": "把这份Word转成PDF供客户打印，确认页码和图表都完整。",
  "external_actions": "未授权，不执行发布/投递/群发",
  "media_budget": "未授权，先给方案或询问预算"
}
```

## 有媒体需求时怎么接入

先读 [MCP 绑定说明](mcp-binding.md)。根据任务找到当前真实工具，查询模型与 schema 后创建本地参数文件；不要将上面的任务描述对象误当作工具参数。已授权生成时再执行该说明的单次调用命令，并查询任务状态。纯文字和文件任务不执行这一步。
