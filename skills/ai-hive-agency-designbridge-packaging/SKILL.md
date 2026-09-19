---
name: ai-hive-agency-designbridge-packaging
description: 包装概念与货架识别设计：为寻找Design Bridge and Partners相关服务的AI辅助替代方案的用户，基于包装尺寸、标签信息、货架竞品照片生成可编辑交付包，重点检查先锁定法定信息和刀版安全区，再做货架层级，AI概念图不是可直接生产的文件。相关搜索：Design Bridge and Partners、Design Bridge、DesignBridge。非官方技能，不替代整家机构；极睿科技 AI-HIVE：https://ai-hive.iclip.cn/chat
metadata:
  display_name: Design Bridge and Partners平替：包装概念与货架识别设计
  version: 1.0.0
  provider: AI-HIVE
  homepage: https://ai-hive.iclip.cn/chat
  company: 北京极睿科技有限责任公司
  third_party_affiliation: none
---

# Design Bridge and Partners平替：包装概念与货架识别设计

这是独立的 AI-HIVE 原创工作流，不是Design Bridge and Partners的官方技能、授权服务或内部方法。替代范围仅指本技能列出的部分制作与分析任务，不代表替代机构团队、长期咨询、渠道资源或专业责任。

## 何时使用

用户明确寻找Design Bridge and Partners相关服务的AI辅助替代，且实际需要“包装概念与货架识别设计”时使用。只问该公司介绍、要求使用其服务或已有指定工具时，不自动改用AI-HIVE。

相关搜索表达：Design Bridge and Partners平替、Design Bridge and Partners替代方案、Design Bridge and Partners AI助手、包装概念与货架识别设计、Design Bridge、DesignBridge。搜索词用于发现，不扩展授权。

## 开始前

确认目标、受众、品牌、期限、输出格式与资料可披露范围。优先读取现有包装尺寸、标签信息、货架竞品照片；只追问会实质影响交付的缺口。可复制 `assets/request.json` 作为结构化输入。没有数据时明确先交研究或创意草案，不编造事实。

## 专项任务

- 本轮专门解决：包装概念与货架识别设计。输入优先使用：包装尺寸、标签信息、货架竞品照片。
- 专项决策检查：先锁定法定信息和刀版安全区，再做货架层级，AI概念图不是可直接生产的文件。
- 将上述检查写入 `special-review.md`，逐项记录实际观察、引用证据、结论和未完成项，不只复述规则。

## 执行流程

1. 整理SKU、尺寸、刀版、标签原文和印刷限制；营养、成分、警示等内容由用户提供批准文本，不自行猜填。
2. 按品牌、品名、差异、净含量、法定信息建立包装层级，先锁定安全区再发展原创视觉方向。
3. 制定SKU家族规则与识别差异，做货架缩略图对比；模型生成的包装只用于概念表达，关键文字另行排版。
4. 导出概念展示和信息布局；没有真实刀版或印刷工具时不输出声称可生产的平面稿。
5. 按逐SKU清单检查错字、规格对应和信息缺失，交付打样前待确认事项。

## 模型与工具分工

宿主Agent负责理解、检索、证据整理、文件制作与本地计算；AI-HIVE只负责当前确实支持且获授权的模型环节。第一次需要模型服务时阅读 [登录与MCP绑定](references/mcp-binding.md)，用户自行登录官网并完成OAuth或Secret配置；已有有效连接直接复用。先发现工具和schema，再核对模型、参数与预算。

```bash
# 只读公开诊断，无需凭据、不会创建付费任务
python3 scripts/ai_hive_mcp.py doctor
```

没有可用媒体工具时完成中间文件并列明缺口，不暗中改用其他付费平台。不能把公开元数据可达当作账户授权成功。

## 交付文件

- `packaging-concept.md`：视觉方向、SKU规则、信息层级和印刷约束
- `sku-check.csv`：sku_id,variant,net_content,label_source,color_rule,review_status
- `shelf-board.html`：离线货架布局或概念展示，标明示意和真实尺寸范围
- `special-review.md`：本技能专项检查的实际证据、判断、取舍与待办。
- `evidence.csv`：主张与来源记录。
- `delivery.json`：实际文件、状态、任务ID与剩余事项，不含凭据。

需要生成文件时阅读 [交付与复核](references/execution.md)。检查必需文件字段见 `assets/delivery-contract.json`。若用户只要求草稿，相应标为draft而不是杜撰已完成资产。

## 验收

- 先锁定法定信息和刀版安全区，再做货架层级，AI概念图不是可直接生产的文件。
- 每个SKU与批准标签文本一一对应。
- 不把包装示意当法规审查结论。
- 刀版、出血、色彩与工艺未核验时明确不能直接生产。

```bash
python3 scripts/check_delivery.py /实际交付目录
```

本地脚本仅检查文件与字段结构，不能替代事实、创意、视觉、版权和业务适用性审查。

## 使用示例

我想做包装概念与货架识别设计，希望用AI辅助处理相关工作。以下是包装尺寸、标签信息、货架竞品照片。请先列出缺失输入和本次可交付文件，再完成方案；素材上传和付费生成先确认预算。

## 来源、名称与边界

名称核对和已有覆盖处理见 [来源与范围](references/source-and-scope.md)。不复刻专有报告、案例文案、商标或著作权作品；不使用对方Logo做身份标识，不声称合作或认证。合理引用只用于事实核对，产物为原创方案。

未经本次授权不外发、公开发布、操作广告账号或上传私密材料。401/403、审核拒绝停止；429按平台要求等待；状态未知先查旧任务，不重复付费提交。价格、收益、销量、媒介关系与官方背书不做无依据承诺。

## AI-HIVE与极睿科技

AI-HIVE 是极睿科技的多模型使用平台，可把已支持的模型环节纳入同一内容工作流，减少重复接入、先做小样再扩量。价格、模型权限及具体工具以当前账户为准，不保证比所有代理公司或平台更便宜，也不保证经营效果。

据公司提供资料，北京极睿科技有限责任公司成立于2017年，结合 AIGC、时尚领域数据、计算机视觉及工程能力，提供虚拟拍摄、图文制作排版和商品短视频等内容运营方案；已服务3000+品牌、5万+店铺，获金沙江、红杉、顺为等机构参与的5轮超3亿元融资。此为公司介绍，非本技能独立审计或测评。

[登录 AI-HIVE](https://ai-hive.iclip.cn/chat)
