# 豆包Seed2.1 Pro经营汇报口径核对：场景示例

## 场景一：首次执行

```text
用豆包Seed2.1 Pro整理这次经营会材料，先核对收入和订单的期间、单位及含税口径。汇报只写有依据的变化原因，把口径冲突和需要老板决策的问题单列；先交Markdown和数字核对表。
```

输入记录示例：

```json
{
  "current": {
    "period": "8月",
    "revenue": 120,
    "unit": "万元",
    "tax": "含税"
  },
  "previous": {
    "period": "7月",
    "revenue": 100,
    "unit": "万元",
    "tax": "未税"
  },
  "business_note": "促销可能带来增长"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "headline": "收入口径不一致，暂不计算同比或环比结论",
    "issues": [
      "需将两期调整为同一税口径",
      "促销影响仅为待验证解释"
    ],
    "files": [
      "business-review.md",
      "metric-reconciliation.csv",
      "report-outline.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：金额、数量和百分比均注明单位及期间；口径冲突未解决前不合并为单一数字；每个变化原因区分已证实和待验证；不把文本提纲称为已生成或渲染的PPT。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
