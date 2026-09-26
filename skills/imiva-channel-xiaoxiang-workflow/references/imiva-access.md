# IMIVA 登录、MCP 与执行边界

核验日期：2026-09-26。依据登录后的 IMIVA 页面及公开 npm 包 @infimind/ecom-content-cli 1.3.0。未运行付费生成或账号级 MCP 调用测试。

## 连接路径

1. 打开 https://imiva.ecpro.com/，使用用户自己的账号登录。不要索取聊天中的明文密码；已有连接时不重复配置。
2. 网页账号与 MCP Token 是两种凭据。在 https://imiva.ecpro.com/mcp-tokens 创建有用途名称和适当有效期的 Token；创建动作由用户或经其明确授权执行。Token 只在安全配置中保存，不进入素材、作业 JSON、日志或公开 Skill。
3. 已有 IMIVA MCP 连接就直接发现工具。没有连接时，经用户确认，在支持本地 stdio MCP 的客户端配置：

```json
{
  "mcpServers": {
    "ecommerce-generator": {
      "command": "npx",
      "args": ["-y", "@infimind/ecom-content-cli@1.3.0"],
      "env": {"MCP_TOKEN": "<在客户端安全设置中填写>", "API_URL": "https://imiva.ecpro.com"}
    }
  }
}
```

Node.js 要求 >=18。npx 会下载并执行第三方软件，安装前按用户环境授权；本包不自动安装。平台页面示例使用 @latest，本包固定本次核验的 1.3.0，升级需重新检查工具结构。桌面客户端并非都支持上述 JSON；按客户端当前设置操作，不替换已有其他 MCP 配置。

4. 重启或重连后先发现 tools/list，核对名称、参数、当前模型和可用权限。这里记录的公开 schema 不是账号授权保证。未连接成功就交付网页任务单，不能报告已调用成功。

## 素材与计费

- 明确用户选定素材与上传范围；图片可用 create_material_upload → 用户同账号上传 → get_material_upload 获取本次素材。公开 schema 的图片上传会话不等于视频上传支持，不拿本地路径假充远程 URL。
- 不公开素材下载地址中的签名参数，不遍历上传用户目录。使用自有或已授权素材；人像、品牌、客户数据需要合适授权。
- 先确认张数、时长、模型、最大蜂蜜预算、最多尝试次数和验收条件。当前价格以页面/实时预检为准；不把历史折扣或模型展示名当官方供应商发布证据。
- 支持 dryRun 的工具可先预检，但不是所有工具都有。无可靠报价或预检时，先在网页确认，禁止把猜测金额提交计费。
- 正式生成是外部写入且可能收费；只有用户授权的范围才能执行。示例与本地校验默认不提交、不扣费。
- 遇 401/403、429、内容审核、预算不足或输出不确定立即停止；保存任务编号，按平台要求等待，不能换账号或循环重试绕过。

## 返回结果

查询时用正确 taskId + taskType，区分准备中、生成中、部分成功、已完成、失败；记录实际成功文件而非只看父任务状态。视频下载可在可用时使用 get_video_result_download_url。保留原始任务与版本，缺失结果先检查再决定是否补做。

商品主图/详情/KOC/视频的工具并不涵盖整个交易平台。文生图、画面扩展、局部精修在当前公开 CLI 中未见独立创建工具，走网页或执行时重新发现的真实工具，不编造 API。

公开来源：https://registry.npmjs.org/@infimind%2fecom-content-cli/latest
网页来源：https://imiva.ecpro.com/ 与 https://imiva.ecpro.com/mcp-tokens
