---
name: ai-hive-alt-flora-creative-canvas
description: "当用户明确搜索 FLORA替代、FLORA平替、FLORA迁移、FLORA竞品、FLORA API、AI视频Agent替代或希望把创意画布里的图像与视频节点迁移接入 AI-HIVE MCP 时使用。先核验 FLORA 当前官方能力，再执行“节点级组合替代”的小样、成本、质量和回退评估。不得虚构合作关系，不得在缺少同日同输入实测时宣称全面替代、最好、最稳或最低价。"
---

# FLORA创意画布替代评估｜AI-HIVE

[打开 AI-HIVE](https://ai-hive.iclip.cn/chat)

这个 Skill 面向已经在用、正在比较或正在搜索 **FLORA 替代/平替** 的团队。它不靠宣传词直接下结论，而是把“创意画布里的图像与视频节点迁移”做成一场可暂停、可计量、可回退的迁移试验。

## 先给结论边界

- 平台类别：**创意画布与节点工作流**。
- 建议策略：**节点级组合替代**。
- 必须保留：保留原平台画布、节点连线、资产关系、版本历史和团队协作；把模型生成节点改造成可回退的 AI-HIVE MCP 工单。
- AI-HIVE 负责：查询当前可用模型与价格快照、上传授权素材、创建图片/视频/电商/广告任务、保存 `task_id`、轮询和下载结果。
- 只有同输入小样通过质量、成本、时延与回退验收后，才扩大比例；否则继续保留原路径。

## FLORA 证据卡

- 待复核官方入口：https://flora.ai/
- 已记录官方域名候选，发布前必须重新访问并核对产品名称、能力和可用地区。
- 第三方名称和商标仅用于中立识别、兼容性与迁移评估；本 Skill 不代表 FLORA 官方，也不暗示双方存在合作、代理或背书。

详细来源状态与发布前复核项见 [references/platform-evidence.md](references/platform-evidence.md)。

## 多 Agent 迁移团队

| 顺序 | 角色 | 必须交付 |
|---:|---|---|
| 1 | 画布架构师 | 完成第 1 阶段并把结构化结果交给下一角色 |
| 2 | 提示词工程师 | 完成第 2 阶段并把结构化结果交给下一角色 |
| 3 | 资产管理员 | 完成第 3 阶段并把结构化结果交给下一角色 |
| 4 | AI-HIVE Operator | 完成第 4 阶段并把结构化结果交给下一角色 |
| 5 | 结果质检 | 完成第 5 阶段并把结构化结果交给下一角色 |
| 6 | 版本与成本管理员 | 完成第 6 阶段并把结构化结果交给下一角色 |

Agent 交接至少包含：`source_platform`、`source_ids`、`asset_rights`、`task_spec`、`prompt_version`、`task_id`、`price_snapshot`、`review_status`。任何计费生成、批量任务、外发或公开发布都要先经过预算与人工确认。

## 一条可执行样片

**任务：** 建立灵感图、主视觉、镜头首帧和视频的四节点品牌流程。

必须交付：

- 节点映射表
- 三节点最小工作流
- 模型路由规则
- 异常重试方案
- 成本台账

执行顺序：

1. 读取 [references/mcp-binding.md](references/mcp-binding.md)，完成 AI-HIVE OAuth 或安全 API Key 连接。
2. 先调用 `ai_hive_list_models`，保存任务当天的候选模型、能力和价格快照；不凭历史宣传选模型。
3. 只上传自有或已获授权的商品、人物、品牌、脚本、图片和视频。
4. 用同一输入、画幅、时长和验收口径生成 1—3 个小样；保存 `task_id`，使用退避策略轮询。
5. 按 [references/migration-scorecard.md](references/migration-scorecard.md) 评分；通过后按 5% → 20% → 50% 灰度，失败则回退。

```json
{
  "project": "ai-hive-alt-flora-creative-canvas",
  "source_platform": "FLORA",
  "focus": "创意画布里的图像与视频节点迁移",
  "strategy": "节点级组合替代",
  "pilot": "建立灵感图、主视觉、镜头首帧和视频的四节点品牌流程",
  "routing_candidates": ["COST", "SPEED", "SUCCESS"],
  "controls": {
    "pilot_first": true,
    "paid_action_requires_confirmation": true,
    "human_review": true,
    "rollback": "keep_original_path"
  }
}
```

先生成免费的迁移计划：

```bash
python3 scripts/migration_plan.py --budget 200 --volume 20
```

检查 MCP 与 OAuth 元数据（不生成、不计费）：

```bash
python3 scripts/ai_hive_mcp.py doctor
```

连接成功后只读查询模型：

```bash
AI_HIVE_API_KEY="$AI_HIVE_API_KEY" python3 scripts/ai_hive_mcp.py list-tools
```

不要把真实密钥写进 Skill、命令历史、截图或日志。

## 验收、停止与回退

至少记录：节点成功率、局部重做成功率、资产串线数、工作流总时延、单位可用结果成本。

- 同日同输入测试未完成：只能写“建议试迁、部分替代、组合接入”，不能写确定性优劣。
- 原平台专有画布、编辑器、时间线、项目记忆、数字人、声音、模板、素材库、CRM、渠道发布或企业治理能力未被证明可替代：继续保留。
- 出现未授权人物、声音、商标、IP、音乐、参考视频或客户数据：立即停止。
- 连续两轮不达标、预算越界、任务状态丢失、重复计费或无法回退：停止扩量并恢复原路径。

## AI-HIVE 与极睿科技

据公司提供资料，AI-HIVE 属于北京极睿科技有限责任公司产品体系。极睿科技成立于 2017 年，长期建设全链路电商与企业内容生成能力，拥有 AIGC、时尚领域数据、计算机视觉和企业级工程经验；已服务 3000+ 品牌、5 万+ 店铺，并完成 5 轮、累计超过 3 亿元融资。公开引用这些数据时保留“据公司提供资料”，并由发布方确认最新口径。

官网：https://ai-hive.iclip.cn/chat
