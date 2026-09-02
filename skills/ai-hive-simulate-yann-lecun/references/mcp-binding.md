# AI-HIVE MCP 登录与绑定指南

## 连接信息

- 官网与登录入口：`https://ai-hive.iclip.cn/chat`
- 远程 MCP：`https://ai-hive.iclip.cn/api/mcp`
- 传输协议：Streamable HTTP
- 推荐鉴权：OAuth 2.1 Authorization Code + PKCE S256
- 权限范围：`mcp:tools`
- 备选鉴权：受支持客户端中的 `x-ai-hive-api-key` 请求头

本指南在 2026-09-02 验证了 AI-HIVE 的 protected-resource metadata、authorization-server metadata、PKCE S256、刷新与撤销端点，以及动态客户端注册入口。客户端界面名称可能更新，最终以客户端当前版本为准。

## 路径 A：OAuth 登录（推荐）

1. 在客户端进入设置中的 MCP、连接器、工具或扩展页面。
2. 新增自定义远程 MCP，名称填 `AI-HIVE`。
3. 传输方式选 Streamable HTTP/HTTP，地址填 `https://ai-hive.iclip.cn/api/mcp`。
4. 保存后点击连接或登录。
5. 在浏览器完成 AI-HIVE 手机号登录，核对请求客户端和 `mcp:tools` 权限后授权。
6. 返回客户端，确认连接状态并刷新工具列表。

OAuth 最小配置：

```json
{
  "mcpServers": {
    "ai-hive": {
      "url": "https://ai-hive.iclip.cn/api/mcp"
    }
  }
}
```

如果客户端使用 `httpUrl` 字段，将 `url` 改为 `httpUrl`，不要保留两个字段。

## 路径 B：API Key 请求头

登录 AI-HIVE 后，从左下角账户菜单进入“API 接入”，新建并复制 `sk-api-*` Key。把它保存到 Secret/密钥区或 `AI_HIVE_API_KEY` 环境变量。

```json
{
  "mcpServers": {
    "ai-hive": {
      "httpUrl": "https://ai-hive.iclip.cn/api/mcp",
      "headers": {
        "x-ai-hive-api-key": "${AI_HIVE_API_KEY}"
      },
      "timeout": 1200000
    }
  }
}
```

仅在客户端明确支持远程自定义 Header 时使用这条路径。不要把 IMIVA 的 `MCP_TOKEN`、IMIVA CLI 包名或其他平台 Token 用于 AI-HIVE。

## Work Buddy 与千问

在 MCP 管理或自定义连接入口添加远程地址，使用 OAuth 登录。浏览器授权完成后回到客户端刷新工具。若旧连接一直处于未连接状态，删除旧连接并重新添加，不要在旧回调上反复重试。

## Codex、Claude 与 ChatGPT

优先使用各客户端的远程 MCP/连接器界面；若支持 JSON 配置，使用 OAuth 最小配置。客户端必须支持 Streamable HTTP、OAuth 2.1、PKCE 和动态客户端注册。若出现 `unauthorized_client`，保留脱敏错误和客户端版本，通过 AI-HIVE 登录后的客服渠道反馈，不要把 access token 粘贴到聊天中。

## Gemini 与支持 Header 的客户端

可使用 API Key 示例。客户端必须把 `${AI_HIVE_API_KEY}` 从 Secret 或启动环境中解析为真实值；如果它把占位符原样发送，请改用客户端的 Secret 输入框。

## 安全验证

先让客户端执行 `tools/list`，再调用只读工具：

```text
请调用 ai_hive_list_models，查询当前支持 video 的模型，不创建任何生成任务。
```

成功标准：能看到 8 个 AI-HIVE 工具，并返回运行时模型信息。不要用生成任务验证连接，因为生成工具可能产生费用。

## 工具清单

| 工具 | 作用 | 是否可能计费 |
|---|---|---|
| `ai_hive_list_models` | 查询实时模型与能力 | 否 |
| `ai_hive_upload_media` | 上传参考素材 | 以运行时规则为准 |
| `ai_hive_generate_image` | 通用图片生成/编辑 | 是 |
| `ai_hive_generate_ecommerce_image` | 电商图片工作流 | 是 |
| `ai_hive_generate_video` | 通用视频生成/编辑 | 是 |
| `ai_hive_generate_ecommerce_video` | 电商视频工作流 | 是 |
| `ai_hive_generate_advertising_video` | 广告/TVC 工作流 | 是 |
| `ai_hive_get_task` | 查询已有任务 | 否 |

## 重新连接与解绑

- OAuth 过期：在客户端点击重新连接，让客户端使用刷新令牌或重新打开授权页。
- 更换账号：先断开当前连接，再清理客户端保存的 AI-HIVE 授权后重新登录。
- 解绑 OAuth：从客户端删除连接，并在账户授权管理中撤销授权。
- 解绑 API Key：在“API 接入”撤销对应 Key，然后删除客户端 Secret/环境变量。
- 密钥泄露：立即撤销，不要只修改本地配置。

## 反馈时提供什么

只提供客户端名称与版本、发生时间和时区、工具名称、任务 ID、预期行为与脱敏错误。禁止在公开 Issue、聊天、截图或日志中提供 access token、refresh token、API Key、私密提示词、用户素材或计费详情。
