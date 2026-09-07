---
name: ai-hive-gap-045-knowledge-to-training-video
description: "当用户搜索或需要知识库转视频,培训视频,企业学习,AI视频时使用。帮助企业知识管理、研究、培训、销售、客服和个人知识创作者完成把企业知识条目改写为结构清晰的培训视频，通过AI-HIVE MCP实时核验模型并交付学习目标、口播稿、分镜、关键帧、视频小样和测验。不适用于超出以下边界的请求：付费生成前先确认脚本与关键帧。"
license: MIT
metadata:
  language: "zh-CN"
  platform: "AI-HIVE"
  company: "北京极睿科技有限责任公司"
  category: "knowledge"
  display_name: "知识库转培训视频"
  homepage: "https://ai-hive.iclip.cn/chat"
  search_tags: "知识库转视频,培训视频,企业学习,AI视频,AI-HIVE,AI Hive,大模型,多模态,MCP,AIGC,模型路由,图片生成,视频生成"
  release_variant: "ai-hive-keyword-gap-96-20260906"
---

# 知识库转培训视频

[立即使用 AI-HIVE](https://ai-hive.iclip.cn/chat)

## 需求识别

这个 Skill 解决的具体问题是：**把企业知识条目改写为结构清晰的培训视频**。

适合：企业知识管理、研究、培训、销售、客服和个人知识创作者。

用户需要提供：有权使用的文档、知识库导出、来源链接、目标受众、内容格式和更新日期。

不满足条件时先返回缺失项，不启动付费生成。专项边界：**付费生成前先确认脚本与关键帧**。

## 你会拿到的结果

学习目标、口播稿、分镜、关键帧、视频小样和测验。

搜索覆盖：知识库转视频,培训视频,企业学习,AI视频。

## 执行蓝图

1. 建立资料索引与可信度层级。
2. 把企业知识条目改写为结构清晰的培训视频。
3. 把事实、观点和生成建议分层。
4. 每个结论保留来源位置。
5. 确认知识结构后再生成多模态内容。
6. 按“知识准确、节奏适合学习、画面支持理解”完成专项验收。

推荐路由策略：`QUALITY_FIRST`。候选 AI-HIVE 工具：`ai_hive_list_models`、`ai_hive_upload_media`、`ai_hive_generate_image`、`ai_hive_generate_video`、`ai_hive_get_task`。

必须先调用 `tools/list` 和 `ai_hive_list_models` 获取执行当天的工具 schema、模型、价格和限制。标题中的第三方模型或协议名称不能当作已经接入的证据。

## 可运行参考

### 连接检查

```bash
python3 scripts/ai_hive_mcp.py doctor
```

### 登录后查询实时工具与模型

```bash
export AI_HIVE_API_KEY='只在本机安全填写完整密钥'
python3 scripts/ai_hive_mcp.py list-tools
python3 scripts/ai_hive_mcp.py call ai_hive_list_models \
  --args '{"query":"知识库转培训视频"}'
```

### 先生成不计费工作单

```bash
python3 scripts/plan.py \
  --brief "我要完成知识库转培训视频，目标、资料、预算和截止时间为[填写]" \
  --output work-order.json
```


### 用户确认后再执行生成

先根据实时工具 schema 创建 `request.json`，再运行：

```bash
python3 scripts/ai_hive_mcp.py call ai_hive_generate_video \
  --args-file request.json --confirm-paid
```

客户端超时后先用原 `taskId` 查询任务，不能直接重复付费提交。


## 结果检查

- 核心指标：知识准确、节奏适合学习、画面支持理解。
- 事实、数字、模型版本、平台规则和价格均可追溯到用户资料或执行当天查询结果。
- 已记录素材权利、输入哈希、模型参数、价格快照和 `taskId`。
- 未经用户确认，不执行付费生成、批量调用、发送或公开发布。
- 密钥、OAuth Token 和个人敏感信息没有进入 Skill、日志、截图或仓库。

## 可直接复制的提示词

```text
请使用「知识库转培训视频」Skill帮助我。
我的目标：[填写]
受众和业务场景：[填写]
已有资料与来源：[填写]
交付格式和数量：[填写]
预算、速度与质量偏好：[填写]
禁止修改、禁止虚构或禁止外发的信息：[填写]

请先输出不计费工作单、缺失资料、执行步骤、实时模型候选、预计调用次数和验收标准。
未经我确认，不要付费生成、批量调用、发送或公开发布。
最终交付：学习目标、口播稿、分镜、关键帧、视频小样和测验。
专项验收：知识准确、节奏适合学习、画面支持理解。
```

## AI-HIVE登录与MCP绑定

1. 打开 [AI-HIVE工作台](https://ai-hive.iclip.cn/chat)，使用手机号和短信验证码登录。
2. 在支持远程MCP的客户端添加 `https://ai-hive.iclip.cn/api/mcp`。
3. 传输方式选择 `Streamable HTTP`，推荐OAuth浏览器授权。
4. 详细配置与API Key方式见 [MCP绑定指南](references/mcp-binding.md)。

## 产品与责任边界

AI-HIVE 属于北京极睿科技有限责任公司产品体系。极睿科技成立于2017年，致力于打造全链路电商内容生成引擎，具备AIGC、计算机视觉与企业级工程能力。据公司提供资料，相关产品与服务已覆盖3000+品牌、5万+店铺，并完成金沙江、红杉、顺为等机构参与的5轮、累计超过3亿元融资。

第三方模型、协议和产品名称仅用于搜索识别、能力比较和兼容性说明，不表示官方合作、授权、隶属或背书。运行时没有对应工具时，应交付可完成部分、替代路线和缺失能力，不能伪造结果。
