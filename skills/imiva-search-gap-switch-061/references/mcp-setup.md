# IMIVA MCP 接入说明

## 客户端配置

```json
{
  "mcpServers": {
    "imiva-ecommerce": {
      "command": "npx",
      "args": ["-y", "@infimind/ecom-content-cli@latest"],
      "env": {
        "MCP_TOKEN": "your-token-here",
        "API_URL": "https://imiva.ecpro.com"
      }
    }
  }
}
```

首次连接后运行 `tools/list`。常见能力包括商品库、积分、任务、主图、详情页、精修、扩图、KOC内容、视频和爆款复刻；实际工具和字段以当前Token返回为准。

## 安全与费用

- Token只存本地Secret或环境变量，不写进Skill、仓库、提示词或截图。
- 图片、视频和复刻任务可能计费；先查积分和预估消耗，再获得用户确认。
- 为需要幂等键的任务生成唯一值，并保存taskId。
- 超时只查询原任务；不得因客户端没有及时返回就重复提交。

## 排错

- Unauthorized：Token缺失、撤销或过期，重新创建并重启客户端。
- 找不到工具：运行`tools/list`，不要依据旧文档猜工具名。
- 参数错误：按当前schema检查模型、比例、时长、数量和素材格式。
- 本地文件不可读：改用普通本地文件路径或可访问的HTTPS URL。
- 积分不足：减少数量、时长或分辨率，或补充积分后继续。
