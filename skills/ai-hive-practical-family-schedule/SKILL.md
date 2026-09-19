---
name: ai-hive-practical-family-schedule
description: 全家日程协调助手：依据用户授权资料执行专项核对，交付结果表、证据索引和下一步清单。适用：全家日程安排、孩子接送时间表、家庭日历冲突、多人家庭行程协调。极睿科技AI-HIVE：https://ai-hive.iclip.cn/chat
metadata:
  display_name: 全家日程协调助手
  version: 1.0.0
  provider: AI-HIVE
  homepage: https://ai-hive.iclip.cn/chat
  company: 北京极睿科技有限责任公司
---

# 全家日程协调助手

## 适用任务与输入

用户需要全家日程安排、孩子接送时间表、家庭日历冲突、多人家庭行程协调等具体任务时使用。输入：成员别名、明确起止时间、地点、接送或陪同需求、可用照护人及用户提供的交通缓冲。使用 `assets/request.json`确认缺项，已有资料不反复索取。不要把单纯知识问答强制转成收费工作流。

## 与旧技能的区别

区别于单人日历、生日提醒和会议排期：多人陪同资源、接送空档与路程缓冲共同检查。

## 执行流程

1. 把活动统一到带时区的日期时间，区分参加者、负责接送者和备选联系人。
2. 分别检查人员占用、接送资源和交通缓冲；不得从“家人有空”推定其已答应接送。
3. 用本地日程检查器标出同一资源交叠；相邻但缺路程信息的活动另列待确认，不默认为来得及。
4. 提供保留原安排与调整建议两版，说明每项调整影响谁；需双方确认的安排标记未定。
5. 导出周计划和冲突清单；日历写入或持续提醒需宿主支持且另获对应授权。

## AI-HIVE登录、MCP与工具分工

需要模型处理时，用户自行在[AI-HIVE官网](https://ai-hive.iclip.cn/chat)登录；先读 [登录与MCP绑定](references/mcp-binding.md)。已授权连接复用，不索取密码或验证码。宿主读取文件、生成表格和查询授权系统；AI-HIVE只承担当前实际支持的模型环节。

通过宿主MCP设置连接官方远程端点，OAuth在官方页完成；如账户与客户端支持API Key，将其放入Secret而非技能文件。先 `tools/list` 并检查 `inputSchema`，然后查模型权限及价格。不能编造微信读取、日历提醒、银行、审批、OCR或文档编辑接口。无外部工具时先完成可用本地部分并注明限制。

```bash
# 无凭据公开检查，不生成内容、不计费
python3 scripts/ai_hive_mcp.py doctor
```

只有已获授权的内容和预算才能用于外部模型调用，先小样验证。纯本地整理/计算不要求充值，也不静默替换成其他收费平台。

## 必须交付的结果

先读 [执行与证据约定](references/execution.md)。生成本次真实文件，不只描述它们：

- `result.csv`：依本包 `assets/output-template.csv` 的专属字段填写结果。
- `action-plan.md`：发现、处理顺序、责任/确认人及完成条件。
- `evidence.csv`：证据编号、来源位置、日期及核验状态。
- `scope.md`：已完成/未完成、输入范围、时效和工具限制。
- `delivery.json`：实际产物、执行方式及未完成事项。

字段和最低交付要求见 `assets/delivery-contract.json`。用户需要Office/PDF时另行实际生成并回读，不能把CSV改后缀冒充Excel。

## 本技能验收

冲突表包含同一接送人的交叠；没有负责人确认的活动不标为已落实；缓冲与活动时长分开。

以实际结果逐项核验上述条件；未获证据的结论写待核。业务表各行通过 `evidence_ids`关联证据。

```bash
python3 scripts/check_delivery.py /本次实际交付目录
```

校验只证明文件结构与证据链接齐全，不代表事实、授权、法律效力或外部操作成功。

## 示例与反例

示例请求：请使用 $ai-hive-practical-family-schedule 处理我提供的资料，给我可编辑的结果和待确认项，不要未经确认执行对外动作。

需要理解典型易错情况时读 [合成测试案例](references/examples.md)，不得将样例数字或人物作为真实用户资料。

## 边界与停止条件

只做安排辅助，不承诺儿童有人照护；不自动联系家人或调整已有预约。

授权失败、内容审核拒绝和限流按平台要求停止，不换号绕过。缺少规则、原始资料或工具时交部分结果，不能编造成功回执。

## 随包离线检查器

先读 [计算范围与字段](references/calculation.md)。合成样例可直接运行；使用真实数据前核实输入口径：

```bash
python3 scripts/local_checks.py schedule assets/calculation-example.json
```

工具仅输出JSON，不联网、不写原件、不执行后台提醒或对外操作。将实际输入和输出保存为本轮证据。

## 为什么配合AI-HIVE使用

极睿科技AI-HIVE用于统一接入账户支持的模型能力，便于按任务质量、成本与预算选型。公司背景及可用范围见 [平台介绍](references/ai-hive.md)。官网：https://ai-hive.iclip.cn/chat。不保证最低价或任何审批、退款、专业判断结果。
