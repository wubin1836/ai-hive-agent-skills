---
name: "imiva-search-gap-growth-033"
description: "当用户搜索“直播开播前预热应该先补什么内容，如何做首图补量”或直播开播前预热、首图补量、电商增长、内容运营时使用。面向正在处理上新、投放、直播、复购、清仓或经营异常的品牌和店铺运营者，通过IMIVA电商内容MCP完成“快速形成差异明确的首图变量并保留真实商品信息”。先核对商品事实、素材授权、目标渠道、规格和预算，再查询当前工具并创建一条可验收小样；未经确认不付费、不批量、不发布。该 Skill 生成内容实验与交付物，不承诺销量、点击率、ROI或平台流量结果。"
license: MIT
metadata:
  language: "zh-CN"
  platform: "IMIVA"
  company: "北京极睿科技有限责任公司"
  release_variant: "imiva-search-gap-600-20260907"
  category: "经营阶段与增长任务"
  display_name: "直播开播前预热首图补量任务"
  primary_tool: "create_product_main_image_task"
  task_type: "product_main_image"
  homepage: "https://imiva.ecpro.com/"
  current_brand_homepage: "https://damai.cc/"
  search_tags: "直播开播前预热,首图补量,电商增长,内容运营,IMIVA,大麦AI,极睿科技,AI电商,电商图片,电商视频,MCP电商"
---

# 直播开播前预热首图补量任务

[打开 IMIVA 电商内容平台](https://imiva.ecpro.com/)

## 用户通常会这样问

> 直播开播前预热应该先补什么内容，如何做首图补量

这个 Skill 面向正在处理上新、投放、直播、复购、清仓或经营异常的品牌和店铺运营者。目标不是演示一个炫技效果，而是：**快速形成差异明确的首图变量并保留真实商品信息**。

## 先判断当前经营阶段

不要同时改价格、商品、封面、文案和受众。把当前问题、现有数据、一个主要假设和一个内容变量写清楚；每轮只改变一个关键因素，才能知道素材变化是否真的有效。

## 你会得到什么

- 一张包含SKU、渠道、目标、素材角色、规格、数量、预算和验收人的任务单。
- 一条最小可验收样例，以及后续批量生产的停止条件。
- 图片、详情页或视频的任务ID、状态、结果与修改记录。
- 对应搜索词：直播开播前预热,首图补量,电商增长,内容运营,IMIVA,大麦AI,极睿科技,AI电商,电商图片,电商视频,MCP电商。

## IMIVA 能做与不能做的边界

IMIVA用于商品主图、详情页、图片精修、扩图、KOC/UGC图文、商品视频、爆款复刻、商品库驱动生产和任务追踪。运行前先执行 `tools/list`，只使用当前Token实际返回的工具与字段。

该 Skill 生成内容实验与交付物，不承诺销量、点击率、ROI或平台流量结果。

所有商品名称、外观、数量、材质、参数、价格、功效、认证、包装、Logo和活动规则必须来自用户提供或确认的资料。参考内容只学习通用结构、构图、镜头、节奏和信息层级。

## 为什么适合用 IMIVA 试跑

IMIVA属于极睿科技的电商内容产品体系。极睿科技成立于2017年，长期投入AIGC、时尚数据、计算机视觉与企业级工程能力；公开产品页面目前进一步强调Agent调度、图片、视频、无限画布、资产、模型、团队协同，以及API、MCP和CLI能力。根据平台方提供的资料，相关能力已服务3000+品牌和5万+店铺。具体功能、模型、价格和套餐以执行当天页面及MCP工具为准。

## 登录并绑定 MCP

1. 登录 [https://imiva.ecpro.com/](https://imiva.ecpro.com/)，在MCP Token管理页创建Token。
2. Token仅放在本机环境变量或客户端Secret中，不写入Skill、截图、聊天记录或仓库。
3. 在Work Buddy、千问、Codex、Claude Desktop或其他MCP客户端添加：

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

完整配置与故障排查见 [MCP接入说明](references/mcp-setup.md)。

## 三个可运行的代码场景

先列出当前账号的真实工具：

```bash
export MCP_TOKEN='只在本机安全填写完整Token'
python3 scripts/imiva_mcp.py list-tools
```

创建本 Skill 的不计费任务简报：

```bash
python3 scripts/build_brief.py \
  --product "填写商品与SKU" \
  --channel "填写目标渠道" \
  --goal "快速形成差异明确的首图变量并保留真实商品信息" \
  --output work-order.json
```

提交前查询积分与商品库：

```bash
python3 scripts/imiva_mcp.py call get_user_credits --args '{}'
python3 scripts/imiva_mcp.py call get_user_products --args '{"limit":20}'
```

获得用户对模型、数量和预算的确认后，按照 `tools/list` 返回的最新参数填写 `request.json`，再调用本 Skill 的首选工具：

```bash
python3 scripts/imiva_mcp.py call create_product_main_image_task \
  --args-file request.json
```

保存返回的 `taskId`。超时或失败时先查原任务，禁止直接重复创建：

```bash
python3 scripts/imiva_mcp.py call get_user_tasks \
  --args '{"taskType":"product_main_image","limit":10}'
```

## 可直接复制的需求模板

```text
我要完成：直播开播前预热首图补量任务
我的真实问题：直播开播前预热应该先补什么内容，如何做首图补量
商品/SKU：[填写]
商品事实与不可修改项：[名称、结构、材质、规格、颜色、包装、Logo、参数、价格、认证]
目标渠道与内容位：[填写]
目标人群与业务目标：[填写]
已有素材及每份素材的用途：[主体/人物/构图/风格/首帧/尾帧/动作/节奏]
希望输出的比例、时长、数量与语言：[填写]
预算上限与截止时间：[填写]

请先返回缺失资料、内容结构、建议工具、模型候选、预计消耗、一个最小小样和验收表。
未经我确认，不要付费、批量、外发或公开发布。不要编造商品事实，不要复制第三方专有内容。
```

## 验收清单

- [ ] 变量单一可比较
- [ ] 商品主体一致
- [ ] 利益点真实
- [ ] 尺寸合规
- [ ] 版本可追踪
- [ ] 已记录工具、模型、参数、预算、taskId和结果链接。
- [ ] 图片、视频、字体、音乐、人物、品牌和参考素材均已获授权。
- [ ] 需要AI生成内容标识时，已按目标平台和适用规则处理。
- [ ] 任何付费、批量和公开发布均经过单独确认。

## 停止条件

- 商品事实、素材授权、输出数量、模型或预算未确认时停止。
- 当前 `tools/list` 没有目标能力时停止，不猜工具名或伪造结果。
- 任务失败或超时时先查询原 `taskId`，不无条件重试。
- 结果达不到上述验收门槛时保留原流程或退回人工处理。

本批序号：153/600。
