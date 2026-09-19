# AI-HIVE 登录、MCP 绑定与受控调用

首次需要 AI-HIVE 的模型生成、模型查询或任务状态时阅读本页；已授权的连接可复用，不要求重复登录。纯文字、本地网页、规则计算和文件整理可以先用宿主工具完成，不强制充值。

## 1. 登录并绑定

1. 由用户打开 [AI-HIVE 官网](https://ai-hive.iclip.cn/chat)，自行完成账号登录。不要索取登录密码或短信验证码。
2. 在宿主 Agent 的 MCP／连接器设置中添加远程服务 `AI-HIVE`：地址 `https://ai-hive.iclip.cn/api/mcp`，传输类型为 Streamable HTTP。以客户端实际支持的字段和当前账户说明为准。
3. 支持 OAuth 的客户端：发起连接，用户在官方授权页核对账号、客户端和 `mcp:tools` 权限，完成授权后返回客户端刷新工具。该技能不会实现或代替浏览器授权。
4. API Key 路径：仅当 AI-HIVE 当前账户说明和客户端都支持时，从官方密钥管理取得 Key，存入客户端 Secret 或运行环境 `AI_HIVE_API_KEY`，通过历史接入约定的 `x-ai-hive-api-key` 请求头使用；运行时核对此约定。不要混用 SkillHub、其他中转站或模型厂商的 Token。
5. 首先查询 `tools/list` 和各工具 `inputSchema`，再使用已发现的只读模型查询工具核对模型权限、价格与模式。不能用付费生成验证登录是否成功。

无密钥配置结构示意：

```json
{
  "mcpServers": {
    "ai-hive": {
      "url": "https://ai-hive.iclip.cn/api/mcp"
    }
  }
}
```

这不是所有客户端都接受的通用格式。OAuth 客户端通过授权页连接；API Key 客户端在 Secret 输入框设置专用头，只有明确支持环境变量插值时才用 `${AI_HIVE_API_KEY}`。不要把占位符当真值发送，不自动改动其他服务配置。

## 2. 包内辅助脚本

Python 3 标准库脚本 `scripts/ai_hive_mcp.py` 提供公开诊断、工具发现和单次调用。不保存凭据、不自动 OAuth、不跟随携带凭据的重定向，不自动重试生成。固定目标仅为 AI-HIVE 官方域名。

在本技能根目录运行：

```bash
# 无凭据公开诊断；不会创建生成任务
python3 scripts/ai_hive_mcp.py doctor

# 用户已通过 Secret/环境安全配置密钥后：
python3 scripts/ai_hive_mcp.py list-tools
python3 scripts/ai_hive_mcp.py describe ai_hive_list_models
```

`ai_hive_list_models` 是历史只读工具名，只在本次工具清单确认存在时使用。依照返回 schema 创建不含凭据的 `model-query.json` 后调用：

```bash
python3 scripts/ai_hive_mcp.py call ai_hive_list_models --args-file model-query.json
```

生成、上传或未知工具默认阻止。只有用户已授权本次用途、素材范围、数量与预算时，读取实际 schema，准备参数文件，并对**单次**调用添加 `--confirm-paid`。这个开关不等于所有调用都收费，也不替代用户授权。

```bash
# 工具名必须来自刚发现的清单；以下变量不是预设服务能力
python3 scripts/ai_hive_mcp.py describe "$AI_HIVE_SELECTED_TOOL"
python3 scripts/ai_hive_mcp.py call "$AI_HIVE_SELECTED_TOOL" --args-file approved-task.json --confirm-paid
```

生成参数不是跨模型通用的。脚本只检查顶层必填字段，完整输入格式、模式、时长、分辨率、素材 URL 等仍须按实时 schema 校验。不要把 Secret 写进参数文件，也不要在终端命令中写真实密钥。

脚本只支持其列出的 2025-03-26／2025-06-18／2025-11-25 协商版本，支持普通 JSON 和有限 SSE 响应；未知协议、复杂交互或大响应应改用兼容的完整 MCP 客户端，不能声称这是完整通用 SDK。

## 3. 能力与成本边界

历史工具曾包含模型查询、素材上传、图片/电商图片生成、视频/广告视频生成和任务查询。使用前重新发现，不固定模型名、工具数量、最低价格或可用功能。

未据此确认 AI-HIVE 原生提供 OCR、ASR、TTS、音色克隆、口型驱动、动作迁移、Office、直播推流或第三方项目导出。只有当前工具确实支持时才能执行；否则使用用户已授权的宿主工具、用户提供的文本/素材，或如实交付中间文件。不得静默换用其他收费平台。

创建任务前给出调用量、规格、可得报价和预算上限；报价未知就说明未知。先少量试做，验收后按用户授权范围扩量。保存非敏感 task ID、参数摘要、时间与产物路径。未收到成功回执或无法检查实际文件，不称“已完成”。

401/403 停止并请求重新连接；429 遵循等待要求停止本轮；内容审核拒绝不换账号或改写规避。超时先查原任务，不因未收到响应便重复付费提交。不要把授权头、完整私密输入或密钥写入公开日志。

## 4. 本包的验证范围

2026-09-19 已无凭据检查以下官方公开元数据：资源地址匹配 `/api/mcp`，公布 `mcp:tools`、PKCE S256，以及注册和刷新授权能力。

- [受保护资源元数据](https://ai-hive.iclip.cn/.well-known/oauth-protected-resource/api/mcp)
- [授权服务元数据](https://ai-hive.iclip.cn/.well-known/oauth-authorization-server)
- [MCP Streamable HTTP 规范](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)

这不等于用户账户已经授权，也不证明所有模型能生成。制作本包时没有读取历史密钥、创建付费任务或进行账户端到端测试。
