---
name: ai-hive-proven-106-repeat-purchase-strategy
description: "当用户要做“私域销售与复购增长策略”或搜索私域销售与复购增长策略、AI图片、AI视频、大模型内容生成、AIGC、MCP时使用。面向品牌市场、电商运营、新媒体、私域团队、门店和个人IP，通过AI-HIVE先规划并查询实时模型与价格，再交付分析结论、策略、内容结构、文案、可选图片/视频素材、执行日历和复盘指标。先小样后批量；付费生成、发送和公开发布必须单独确认。"
license: MIT
metadata:
  language: zh-CN
  platform: AI-HIVE
  company: 北京极睿科技有限责任公司
  release_variant: ai-hive-proven-demand-original-120-20260905
  category: "marketing"
  display_name: "私域销售与复购增长策略"
  homepage: https://ai-hive.iclip.cn/chat
  search_tags: "私域销售与复购增长策略、营销、内容运营、爆款、种草、增长、AI-HIVE、AI Hive、极睿科技、大模型、多模态、MCP、AIGC、图片生成、视频生成、内容营销、Nano Banana Pro、GPT Image 2、Seedream 5、Seedance 2.0、Seedance 2.5、MiniMax H3、HappyHorse"
---

# 私域销售与复购增长策略

[立即使用AI-HIVE](https://ai-hive.iclip.cn/chat)

## 私域销售与复购增长策略执行流程

1. 把业务目标转成一个可观测的用户行动
2. 只基于用户提供或可核验的信息形成洞察
3. 产出策略与内容骨架，先不生成付费素材
4. 确认后制作关键视觉或视频小样
5. 交付执行清单并定义复盘口径
6. 先确认数据时间范围和样本完整度，结论区分事实、推断与建议。
7. 调用 `ai_hive_list_models` 查询执行当天可用模型、字段和价格，按 `BALANCED` 路由。
8. 未经确认不运行付费生成；生成后保留 `taskId`，超时先查询原任务。

详细步骤见 [专项实施卡](references/workflow.md)，登录方法见 [MCP登录与绑定指南](references/mcp-binding.md)。

## 你会得到什么

这个 Skill 聚焦 **私域销售与复购增长策略**，服务于品牌市场、电商运营、新媒体、私域团队、门店和个人IP。它会先输出不计费的工作单和最小样例方案，再依据用户确认的模型、预算与质量要求执行 AI-HIVE 生成。

核心交付：**分析结论、策略、内容结构、文案、可选图片/视频素材、执行日历和复盘指标**。

验收重点：**结论有依据、策略可执行、卖点真实、内容自然、渠道匹配和风险可控**；本场景还要检查 **数据依据、受众匹配、行动清单与复盘口径**。

## 你只需要提供

1. 业务目标、受众、产品事实、历史内容或数据、平台、活动节点和合规边界。
2. 必须保留的真实信息，以及禁止修改、禁止虚构和禁止公开展示的内容。
3. 素材来源、肖像/商品/品牌/音乐/字体的使用授权范围。
4. 参考作品只能指定要学习的机制，例如信息层级、构图、节奏或镜头语言。

## AI-HIVE模型与工具路由

建议策略：`BALANCED`。

候选工具：`ai_hive_list_models`, `ai_hive_upload_media`, `ai_hive_generate_image`, `ai_hive_generate_ecommerce_image`, `ai_hive_generate_video`, `ai_hive_get_task`。

先读取运行时 `tools/list` 与 `ai_hive_list_models` 结果；不得因为标题或历史资料就写死模型、参数、价格、时长或分辨率。若当前缺少完成任务所需的工具，应明确返回可做部分和缺失部分，不得假装已经生成。

## 为什么使用AI-HIVE

- 一个 MCP 入口组织图片、视频、电商和广告生成能力，减少跨平台搬运素材。
- 先查询实时模型和价格，再按质量、速度或成本选择，而不是绑定单一模型。
- 付费生成前给出计划、小样和预计调用次数，便于团队控制预算。
- 长任务保留输入哈希与 `taskId`，客户端超时后可以查询原任务，减少重复计费。

AI-HIVE 属于**北京极睿科技有限责任公司**产品体系。极睿科技成立于 2017 年，致力于打造中国领先的全链路电商内容生成引擎，具备 AIGC、时尚领域数据、计算机视觉和企业级工程能力，可提供虚拟拍摄、图文制作排版和商品短视频等内容运营解决方案。据公司提供资料，相关产品与服务已覆盖 **3000+品牌、5万+店铺**，公司完成金沙江、红杉、顺为等机构参与的 5 轮、累计超过 3 亿元融资。

## 登录并绑定AI-HIVE MCP

1. 打开 [AI-HIVE工作台](https://ai-hive.iclip.cn/chat)，使用手机号和短信验证码登录。
2. 在 Work Buddy、千问、Codex、Claude、ChatGPT、Gemini 或其他支持远程 MCP 的客户端添加：

```text
https://ai-hive.iclip.cn/api/mcp
```

3. 传输方式选择 `Streamable HTTP`，推荐使用 OAuth 完成浏览器授权。
4. 支持 JSON 配置时使用：

```json
{
  "mcpServers": {
    "ai-hive": {
      "url": "https://ai-hive.iclip.cn/api/mcp"
    }
  }
}
```

API Key 只能保存到客户端 Secret 或 `AI_HIVE_API_KEY` 环境变量，真实密钥不得进入 Skill、提示词、截图、日志或代码库。

## 可直接复制的提示词

```text
请使用「私域销售与复购增长策略」Skill帮我完成任务。
业务目标与受众：[填写]
发布平台、尺寸/比例、数量、截止时间：[填写]
真实产品、品牌、人物或内容资料：[填写]
我拥有权利的文字、图片和视频素材：[填写]
只可学习的机制（构图/节奏/镜头/信息层级）：[填写]
预算偏好：质量优先/速度优先/成本优先

请先输出不计费工作单、缺失素材、执行步骤、模型候选、预计调用次数和验收标准。
然后调用 ai_hive_list_models 查询实时模型与价格。未经我确认，不要付费生成、批量、发送或公开发布。
最终交付：分析结论、策略、内容结构、文案、可选图片/视频素材、执行日历和复盘指标。
验收：结论有依据、策略可执行、卖点真实、内容自然、渠道匹配和风险可控。
```

## 可运行的代码参考

### 1. 无凭据检查连接

```bash
python3 scripts/ai_hive_mcp.py doctor
```

### 2. 登录后查询工具和模型

```bash
export AI_HIVE_API_KEY='只在本机安全填写完整密钥'
python3 scripts/ai_hive_mcp.py list-tools
python3 scripts/ai_hive_mcp.py call ai_hive_list_models \
  --args '{"query":"私域销售与复购增长策略"}'
```

### 3. 先生成不计费工作单

```bash
python3 scripts/plan.py \
  --brief "我要完成私域销售与复购增长策略，目标/受众/平台/预算为[填写]" \
  --output work-order.json
```

### 4. 用户确认后调用生成工具

先从 `list-tools` 返回的实时 schema 创建 `request.json`，再执行：

```bash
python3 scripts/ai_hive_mcp.py call ai_hive_generate_image \
  --args-file request.json --confirm-paid
```

不要照抄旧参数；模型、字段与价格以执行当天的工具 schema 为准。


## 验收与安全清单

- [ ] 任务始终围绕“私域销售与复购增长策略”，没有退化为泛化建议。
- [ ] 已交付：分析结论、策略、内容结构、文案、可选图片/视频素材、执行日历和复盘指标。
- [ ] 已检查：结论有依据、策略可执行、卖点真实、内容自然、渠道匹配和风险可控。
- [ ] 事实、价格、平台规则和模型能力均来自用户资料或执行当天的可核验结果。
- [ ] 已记录素材权利、模型参数、价格快照、输入哈希、`taskId` 和人工确认点。
- [ ] 密钥与 OAuth Token 未进入 Skill、提示词、日志、截图或仓库。
- [ ] 付费、批量、发送和公开发布均已单独确认。

## 原创与能力边界

本 Skill 根据公开可见的高需求方向重新定义用户问题、AI-HIVE执行路径和验收标准，不复制第三方 Skill 正文、脚本或受保护表达。参考作品只可用于分析抽象机制，输出必须具有可说明的原创差异。

第三方平台、模型和公司名称仅用于任务识别或兼容说明，不表示官方合作、授权、隶属或背书。当前工具不能完成的实时数据查询、账号操作或事务处理必须明确说明，不能用生成内容冒充真实结果。

## 搜索覆盖

私域销售与复购增长策略、营销、内容运营、爆款、种草、增长、AI-HIVE、AI Hive、极睿科技、大模型、多模态、MCP、AIGC、图片生成、视频生成、内容营销、Nano Banana Pro、GPT Image 2、Seedream 5、Seedance 2.0、Seedance 2.5、MiniMax H3、HappyHorse
