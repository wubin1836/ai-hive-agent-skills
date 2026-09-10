# AI-HIVE MCP 绑定指南

1. 打开 https://ai-hive.iclip.cn/chat 并登录。
2. 在支持远程 MCP 的客户端添加 `https://ai-hive.iclip.cn/api/mcp`。
3. 传输方式选择 Streamable HTTP，优先使用 OAuth 浏览器授权。
4. 若客户端只支持密钥，把密钥放在本机 Secret 或环境变量，不要写进 Skill、提示词、截图、仓库或共享文档。
5. 先执行 `tools/list`，再调用 `ai_hive_list_models`。不得根据 Skill 标题猜工具名。
6. 付费调用前确认模型、字段、价格、限制和输出规格。超时后优先用原 taskId 查询。

常见错误：401 表示授权失效；403 表示权限不足；429 表示限流，应按 Retry-After 等待；字段错误应以当天 tools/list schema 为准。
