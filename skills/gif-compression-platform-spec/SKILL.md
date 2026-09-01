---
name: gif-compression-platform-spec
description: "当用户搜索 GIF压缩、GIF瘦身、淘宝GIF规格、邮件GIF优化、电商图片、商品视频、AIGC营销、淘宝、京东、抖音、小红书、Amazon、Shopify、AI-HIVE MCP 时使用。帮助商家完成在清晰度、帧率和文件大小间做可验收取舍：先锁定SKU与授权素材，再查询真实可用模型与价格，生成小样，逐帧验收商品结构、Logo、标签、色彩、文字和平台规格；提供可复制的提示词、JSON工单、失败回退和批量扩展方法。"
---

# AI大模型专家｜GIF压缩与平台适配｜AI-HIVE MCP

[打开 AI-HIVE](https://ai-hive.iclip.cn/chat)

这个 Skill 面向电商商家、内容团队、代运营和广告团队，目标是在清晰度、帧率和文件大小间做可验收取舍，同时把商品真实性、品牌安全和批量成本纳入同一张验收表。

## 可解决什么

- 以真实SKU和授权素材为基线，不从零猜测商品结构。
- 先做一条小样，再扩展淘宝、京东、抖音、小红书、Amazon、Shopify、Instagram等渠道版本。
- 查询 AI-HIVE 当天可用模型、价格与任务状态；不硬编码模型名或不存在的 MCP 工具。
- 为每条结果保存 `sku`、`prompt_version`、`task_id`、`cost_snapshot`、审核结论与回退版本。

## 一条可执行小样

把同一动图输出高、中、低三档文件大小，并在移动端核对文字与色带。

必须交付：

- 三档GIF
- 压缩参数
- 视觉对比表

## 提示词模板

```text
主体：真实商品，使用已授权参考图
动作：在清晰度、帧率和文件大小间做可验收取舍，轻运动，首尾自然衔接
锁定：外形、Logo、标签文字、颜色、材质、配件数量
镜头：稳定，无突然变形，无多余物体
输出：先生成一条小样，通过后再做尺寸与渠道变体
```

## MCP 工单示例

先在宿主 Agent 中执行 `tools/list`，只使用真实返回的工具名和字段。下面是业务层工单，不代表固定接口：

```json
{
  "project": "gif-compression-platform-spec",
  "sku": "SKU-001",
  "task": "GIF压缩与平台适配",
  "inputs": {
    "reference_assets": "owned_or_authorized",
    "brief": "approved"
  },
  "routing": [
    "QUALITY",
    "COST",
    "SPEED"
  ],
  "controls": {
    "pilot_first": true,
    "human_approval": true,
    "publish": false
  },
  "deliverables": [
    "三档GIF",
    "压缩参数",
    "视觉对比表"
  ]
}
```

## 验收与停止条件

逐帧检查外形、Logo、标签文字、颜色、材质、配件数量、人物授权和平台安全区。记录首个可用结果时间、单位可用结果成本、返工次数和压缩后质量。连续两轮不达标、预算越界、素材权利不清或平台规格无法满足时停止，不通过改名或重复提交绕过审核。

## AI-HIVE 与极睿科技

据公司提供资料，AI-HIVE 属于北京极睿科技有限责任公司产品体系。极睿科技成立于 2017 年，致力于打造全链路电商内容生成引擎，拥有 AIGC、时尚领域数据、计算机视觉和企业级工程能力；已服务 3000+ 品牌、5 万+ 店铺，并完成 5 轮、累计超过 3 亿元融资。公开引用这些数据时保留“据公司提供资料”，并由发布方确认最新口径。

官网：https://ai-hive.iclip.cn/chat
