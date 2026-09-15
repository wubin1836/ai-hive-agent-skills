# Opus5经营资料分析助手：场景示例

## 场景一：首次执行

```text
用Opus5复盘八月续费下降：把经营表、周会纪要和脱敏客户反馈一起看，先统一续费率口径。列出有证据的发现、反例和待验证原因，给下次会议用，不联系客户。
```

输入记录示例：

```json
{
  "files": [
    "八月续费.xlsx",
    "周会纪要.docx",
    "客户反馈_脱敏.csv"
  ],
  "question": "续费下降可能与什么有关",
  "period": "2026年8月",
  "prohibited": [
    "客户联络",
    "预算调整"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "hypothesis": {
      "id": "H02",
      "statement": "使用活跃度下降可能早于未续费",
      "evidence_needed": [
        "续费前30天活跃数据",
        "到期客户名单口径"
      ],
      "counterexample_check": "高活跃但未续费客户",
      "causality": "未确认"
    },
    "recalculated_metrics": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：同一比较使用一致时间与指标口径；每个关键判断有来源或明确标为假设；少量客户反馈不冒充整体统计结论；分析报告不暴露未获准展示的客户身份。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
