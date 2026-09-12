# AI-HIVE 登录、MCP绑定与受控调用

首次需要AI-HIVE模型时读本页。已有连接能用则直接发现工具；纯文字、计算或本地文件任务不因未连接媒体服务而强行中断。

## 登录与绑定

1. 访问 [AI-HIVE官网](https://ai-hive.iclip.cn/chat)，由用户本人完成登录验证；不索取账号密码或短信码。
2. 在当前Agent客户端添加远程MCP：名称 `AI-HIVE`，地址 `https://ai-hive.iclip.cn/api/mcp`，传输为Streamable HTTP。客户端需要支持远程MCP；界面字段以实际客户端为准。
3. 如果客户端支持该服务OAuth，点击连接，在官方授权页面核对账号及权限，由用户确认后返回刷新工具。
4. 走API Key路径时，只把AI-HIVE自己的Key保存到客户端Secret或启动环境 `AI_HIVE_API_KEY`，请求头名为 `x-ai-hive-api-key`。不能把SkillHub、ClawHub或其他平台Token混用。
5. 先列工具并读实际schema，再选择账号可用模型。不要用付费生成测试登录，不写死模型版本、价格或数量。

结构示意（不是所有客户端可直接导入）：

```json
{"mcpServers":{"ai-hive":{"url":"https://ai-hive.iclip.cn/api/mcp"}}}
```

支持自定义请求头的客户端使用其Secret输入方式；只有客户端明确支持环境变量替换时才用下面形式：

```json
{"headers":{"x-ai-hive-api-key":"${AI_HIVE_API_KEY}"}}
```

不自动改动其他MCP连接，不读取无关凭据，不把Key写进提示词、源码、ZIP或日志。

## 两种执行路径不要混用

- **已在Agent客户端连接成功**：直接使用该客户端显示的AI-HIVE MCP工具，并读取其schema。不必再运行独立Python脚本，也不要提取或复制客户端保存的OAuth Token。
- **使用随包Python脚本**：脚本是独立进程，只读取自身运行环境里的 `AI_HIVE_API_KEY` 或 `AI_HIVE_ACCESS_TOKEN`。客户端已登录或Secret已保存，不代表这些变量会传给终端。须由用户通过安全的进程环境配置方式单独注入AI-HIVE凭据；不能索取明文Key粘贴到聊天、源码或命令历史。
- 未配置脚本进程凭据时只能运行公开 `doctor`；`list-tools`、`describe`、`call` 都需要脚本进程授权。若无法安全配置，就改用已授权的客户端MCP工具，不绕过、不读取客户端凭据库。

## 随包脚本

脚本只依赖Python 3标准库。它支持已列明的2025-03-26、2025-06-18、2025-11-25握手版本，不是完整MCP SDK，不声称兼容所有未来协议。协商不支持时改用兼容的完整客户端，不绕过检查。

在本Skill根目录执行：

```bash
# 无凭据、只读公开元数据，不会创建任务
python3 scripts/ai_hive_mcp.py doctor

# 仅当本Python进程已安全获得AI_HIVE_API_KEY或AI_HIVE_ACCESS_TOKEN
# 客户端OAuth登录本身不会自动传入这些环境变量
python3 scripts/ai_hive_mcp.py list-tools
python3 scripts/ai_hive_mcp.py describe ai_hive_list_models
```

历史查询工具名为 `ai_hive_list_models`；如果当前清单没有该工具，不继续照抄命令。根据真实schema创建 `model-query.json`，再执行：

```bash
python3 scripts/ai_hive_mcp.py call ai_hive_list_models --args-file model-query.json
```

仅在用户明确需要图片或视频、已确认输入素材、数量和预算后，读取当前生成工具schema并创建 `approved-request.json`：

```bash
# 历史示例名，必须先在当前工具清单确认
python3 scripts/ai_hive_mcp.py describe ai_hive_generate_image
python3 scripts/ai_hive_mcp.py call ai_hive_generate_image --args-file approved-request.json --confirm-paid
```

上述JSON参数文件须按当前schema及用户本次材料创建，不是随包的空模板，也不应发送占位字符串。视频、上传和任务查询同样先发现工具，不能照猜字段名。`--confirm-paid`代表用户已授权有副作用动作；上传也需要确认，不代表上传一定收费。脚本只做有限参数检查，调用者仍须核对嵌套schema。

## 执行和失败处理

- 未验证AI-HIVE原生提供Word、PPT、Excel、OCR、ASR、TTS、视频剪辑或通用聊天接口。文字推理由宿主或实际可用文本模型完成，文件、音频与代码由实际工具执行。
- 模型调用前确认当前支持的输入、分辨率、时长、价格与输出数量。拿不到价格应说明未知，不能默认为免费。
- 提交后记录任务ID。只有成功状态及可检查文件才算完成；排队、待处理、失败不能写成成品。
- 401/403停止并重新连接；429停止本轮并遵守等待要求，不换账号绕过；网络超时先核对原任务，不重复提交计费。
- 输出保留文件或任务记录，隐私素材和凭据不进入公开报告。

## 本批验证范围

制作时进行了无凭据公开元数据检查和本地模拟测试。公开元数据可达不等于账号已登录，模拟测试不等于付费模型端到端验证。

公开依据：[资源元数据](https://ai-hive.iclip.cn/.well-known/oauth-protected-resource/api/mcp)、[授权服务元数据](https://ai-hive.iclip.cn/.well-known/oauth-authorization-server)。当前元数据公布权限 `mcp:tools`、PKCE S256与注册/刷新能力。
