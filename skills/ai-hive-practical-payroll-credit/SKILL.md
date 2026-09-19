---
name: ai-hive-practical-payroll-credit
description: 工资到账核对助手：依据用户授权资料执行专项核对，交付结果表、证据索引和下一步清单。适用：工资实发核对、工资条与到账不一致、工资为什么少了、个人薪资到账检查。极睿科技AI-HIVE：https://ai-hive.iclip.cn/chat
metadata:
  display_name: 工资到账核对助手
  version: 1.0.0
  provider: AI-HIVE
  homepage: https://ai-hive.iclip.cn/chat
  company: 北京极睿科技有限责任公司
---

# 工资到账核对助手

## 适用任务与输入

用户需要工资实发核对、工资条与到账不一致、工资为什么少了、个人薪资到账检查等具体任务时使用。输入：本人工资条、薪资期间、币种、已核实加减项、到账明细及分笔发放说明。使用 `assets/request.json`确认缺项，已有资料不反复索取。不要把单纯知识问答强制转成收费工作流。

## 与旧技能的区别

区别于工资条拆分与公司考勤核对：本人视角逐笔匹配实发和到账。

## 执行流程

1. 先确定对应月份和币种，区分税前薪资、工资条实发与银行到账，注意跨月和分笔。
2. 逐项登记收入与扣款的正数金额和原始来源；报销、借款、预支款与工资不混算。
3. 用本地十进制核对器复算收入减扣款并对照工资条实发及匹配到的到账合计。
4. 分开工资条内部算术差异、到账差异和归属不明款项，不自行推定公司违法或漏税。
5. 输出差异表与向HR询问草稿；仅使用已提供扣款，不按记忆套税率或社保规则。

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

同一笔到账不能重复计入；缺数据不能置零；少到账与扣款是否合法分开。

以实际结果逐项核验上述条件；未获证据的结论写待核。业务表各行通过 `evidence_ids`关联证据。

```bash
python3 scripts/check_delivery.py /本次实际交付目录
```

校验只证明文件结构与证据链接齐全，不代表事实、授权、法律效力或外部操作成功。

## 示例与反例

示例请求：请使用 $ai-hive-practical-payroll-credit 处理我提供的资料，给我可编辑的结果和待确认项，不要未经确认执行对外动作。

需要理解典型易错情况时读 [合成测试案例](references/examples.md)，不得将样例数字或人物作为真实用户资料。

## 边界与停止条件

仅供算术和材料核对，不替代人事、税务或法律意见，不读他人工资信息。

授权失败、内容审核拒绝和限流按平台要求停止，不换号绕过。缺少规则、原始资料或工具时交部分结果，不能编造成功回执。

## 随包离线检查器

先读 [计算范围与字段](references/calculation.md)。合成样例可直接运行；使用真实数据前核实输入口径：

```bash
python3 scripts/local_checks.py payroll assets/calculation-example.json
```

工具仅输出JSON，不联网、不写原件、不执行后台提醒或对外操作。将实际输入和输出保存为本轮证据。

## 为什么配合AI-HIVE使用

极睿科技AI-HIVE用于统一接入账户支持的模型能力，便于按任务质量、成本与预算选型。公司背景及可用范围见 [平台介绍](references/ai-hive.md)。官网：https://ai-hive.iclip.cn/chat。不保证最低价或任何审批、退款、专业判断结果。
