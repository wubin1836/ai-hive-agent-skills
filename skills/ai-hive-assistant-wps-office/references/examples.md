# WPS办公助手：具体任务示例

这些是可交给宿主 Agent 的任务请求，不是伪造的 AI-HIVE API。所有示例均需按当前用户范围执行；媒体生成需要另行明确数量和预算。

## 示例 1：WPS打印异常

```text
WPS里打开这张Excel表打印总少两列，帮我检查并给出可打印版。
```

期望交付：范围和分页诊断、文件或操作清单，注明是否已在WPS验证。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-assistant-wps-office",
  "request": "WPS里打开这张Excel表打印总少两列，帮我检查并给出可打印版。",
  "external_actions": "未授权，不执行发布/投递/群发",
  "media_budget": "未授权，先给方案或询问预算"
}
```

## 示例 2：文档格式转换

```text
这份WPS文档要发给用Word的客户，保留目录、表格和页码。
```

期望交付：目标格式文件与兼容检查，不能验证的字段刷新项被说明。

结构化任务参考（给 Agent 读取，不直接 POST 到 MCP）：

```json
{
  "skill": "ai-hive-assistant-wps-office",
  "request": "这份WPS文档要发给用Word的客户，保留目录、表格和页码。",
  "external_actions": "未授权，不执行发布/投递/群发",
  "media_budget": "未授权，先给方案或询问预算"
}
```

## 有媒体需求时怎么接入

先读 [MCP 绑定说明](mcp-binding.md)。根据任务找到当前真实工具，查询模型与 schema 后创建本地参数文件；不要将上面的任务描述对象误当作工具参数。已授权生成时再执行该说明的单次调用命令，并查询任务状态。纯文字和文件任务不执行这一步。
