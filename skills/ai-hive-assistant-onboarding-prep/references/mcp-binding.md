# AI-HIVE 登录、绑定与单次调用

首次需要模型图片／视频时阅读本页；已经连接且工具可用，不要求用户重复登录。纯文字和本地文件工作可以先完成，不因未登录而强行中断。

## 登录与连接

1. 打开 [AI-HIVE 官网／登录](https://ai-hive.iclip.cn/chat)，由用户本人完成页面上的登录验证，不索取密码或短信码。
2. 在所用 Agent 客户端的 MCP／连接器设置中，添加自定义远程服务：名称 `AI-HIVE`，地址 `https://ai-hive.iclip.cn/api/mcp`，类型 Streamable HTTP。各客户端字段和支持范围不同，以其当前界面为准。
3. 若客户端支持此服务的 OAuth 流程，点击连接，在授权页面核对账号、客户端与 `mcp:tools` 权限，由用户确认；返回客户端刷新工具。
4. 若使用 API Key 路径，在 AI-HIVE 账号当前的 API 接入／密钥管理界面获取 Key，仅存入该客户端 Secret 或环境变量 `AI_HIVE_API_KEY`，通过 `x-ai-hive-api-key` 请求头传递。只有明确支持远程自定义请求头的客户端才能走此路径。不要将其他平台 Token 混用。
5. 先 `tools/list`，检查实时工具及 `inputSchema`；再按返回 schema 调用只读模型查询。工具数量不是固定验收标准，不通过付费生成验证连接。

远程配置结构示意（不是所有客户端都原样接受）：

```json
{
  "mcpServers": {
    "ai-hive": {
      "url": "https://ai-hive.iclip.cn/api/mcp"
    }
  }
}
```

API Key 客户端的补充头示意：

```json
{"headers": {"x-ai-hive-api-key": "${AI_HIVE_API_KEY}"}}
```

仅当客户端文档明确支持环境变量替换时才使用占位符，否则改用 Secret 输入框；不得把占位符当真实 Key 发送。不要自动修改用户其他 MCP 配置、删除已有连接或读取无关密钥。

## 诊断脚本

本 Skill 自带 Python 3 标准库脚本，不自动安装依赖、不启动浏览器 OAuth、不保存 Key、不重试生成。它兼容历史服务握手中的 2025-03-26／2025-06-18／2025-11-25 协议版本，**不声称覆盖最新协议全部特性**。协商出其他版本或客户端需复杂流式能力时，改用兼容的完整 MCP 客户端，不修改凭据目的地址。

在本 Skill 根目录执行：

```bash
# 无凭据，仅检查公开元数据
python3 scripts/ai_hive_mcp.py doctor

# 已通过 Secret/启动环境安全提供 API Key 后，发现工具
python3 scripts/ai_hive_mcp.py list-tools

# 读取模型查询工具真实 schema，不猜 filter、type 或 modelId 参数名
python3 scripts/ai_hive_mcp.py describe ai_hive_list_models
```

根据 `describe` 返回值建立本地 `model-query.json` 参数对象，再执行：

```bash
python3 scripts/ai_hive_mcp.py call ai_hive_list_models --args-file model-query.json
```

只有本次用户要制作媒体并授权数量、用途、素材和预算时，先查看生成工具 schema，准备 `approved-generation.json`：

```bash
python3 scripts/ai_hive_mcp.py describe ai_hive_generate_image
python3 scripts/ai_hive_mcp.py call ai_hive_generate_image --args-file approved-generation.json --confirm-paid
```

这不是可直接提交的通用生成参数样例：`model-query.json`、`approved-generation.json` 需依据账号实时 schema 创建。上传工具也要求 `--confirm-paid`，这个开关表示用户已批准该有副作用的动作，不代表每种上传都收费。脚本只检查顶层必填项，完整参数合法性仍由调用者根据 schema 及服务端确认。

## 已有资料中的工具与能力边界

| 历史工具名 | 用途 | 使用条件 |
|---|---|---|
| ai_hive_list_models | 模型与能力查询 | 只读，运行时核对参数 |
| ai_hive_upload_media | 上传授权素材 | 确认素材范围、隐私和成本规则 |
| ai_hive_generate_image | 通用图片任务 | 查到工具、模型支持目标模式，用户批准预算 |
| ai_hive_generate_ecommerce_image | 电商图片任务 | 同上，保留真实商品关键属性 |
| ai_hive_generate_video | 通用视频任务 | 查询支持的时长、输入和输出限制 |
| ai_hive_generate_ecommerce_video | 电商视频任务 | 当前工具和模型可用时 |
| ai_hive_generate_advertising_video | 广告视频任务 | 当前工具和模型可用时 |
| ai_hive_get_task | 已有任务状态 | 复用已取得的任务 ID，不重复提交 |

这是历史资料清单，不保证当前账号拥有全部工具。**未确认原生 Word、PPT、Excel、OCR、ASR、数字人、TTS 或通用聊天工具。** 若运行时发现新工具，读取其 schema 后才决定使用；否则由宿主 Agent、明确可用的文件工具或用户提供的转写文本完成对应步骤。

创建媒体任务前，给用户看模型、输出数量／规格、价格估计与预算；取不到价格时说明未知，不能默认免费。先小样、验收再扩量。在结果中记录模型 ID、参数摘要、任务 ID 和实际状态；只有收到成功状态且拿到可验证的文件／结果才算交付。队列中、提交中、失败不能写成已生成。

遇 401／403 停止并让用户重新连接；429 按服务等待要求停止当前提交，不换账号绕过；超时或网络断开先核对平台任务记录，不重复触发计费。公开诊断只提供时间、客户端版本、工具名、脱敏错误和非敏感任务 ID，不输出授权头或完整私密提示词。

## 本批核验范围与来源

2026-09-09 仅进行了以下**无凭据公开元数据**检查：

- [资源元数据](https://ai-hive.iclip.cn/.well-known/oauth-protected-resource/api/mcp)：资源为官方 MCP 地址，公布权限 `mcp:tools`。
- [授权服务元数据](https://ai-hive.iclip.cn/.well-known/oauth-authorization-server)：公布 PKCE S256、授权码、刷新与客户端注册端点。

公开元数据可达不等于账号登录或付费模型已端到端验证。本批没有使用历史密钥、没有消耗模型余额。握手说明参考 [MCP 2025-03-26 传输规范](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)；新旧协议有差异，客户端应按服务实际协商版本工作。
