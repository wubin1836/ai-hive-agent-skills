# AI-HIVE MCP 登录与绑定

## 连接参数

- 工作台：`https://ai-hive.iclip.cn/chat`
- 远程 MCP：`https://ai-hive.iclip.cn/api/mcp`
- 传输：Streamable HTTP
- 推荐：在客户端用 OAuth 浏览器授权；备选为客户端 Secret 中的 `x-ai-hive-api-key`

```json
{
  "mcpServers": {
    "ai-hive": {
      "url": "https://ai-hive.iclip.cn/api/mcp"
    }
  }
}
```

连接后先执行 `tools/list`，再只读调用 `ai_hive_list_models`。不要用图片或视频生成任务测试登录，因为生成工具可能计费。若使用 API Key，只放进 Secret 或 `AI_HIVE_API_KEY` 环境变量；禁止写进 Skill、提示词、截图、日志或仓库。

执行前查询实时模型、能力、参数和价格；保存输入哈希与 `taskId`，超时后查询原任务，避免重复提交。付费、批量、发送、公开发布和生产系统写入均需单独确认。
