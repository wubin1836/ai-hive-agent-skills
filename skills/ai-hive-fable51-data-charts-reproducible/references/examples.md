# Fable数据分析与图表助手：场景示例

## 场景一：首次执行

```text
用Fable5.1分析这份门店销售.csv，比较近12周各门店的客单价和销售额。退款按负数保留，重复订单先列出来别直接删。给清洗数据、能复跑的脚本和图表报告。
```

输入记录示例：

```json
{
  "file": "门店销售.csv",
  "period": "最近12周",
  "metrics": [
    "销售额",
    "客单价"
  ],
  "group_by": "门店",
  "refund_policy": "负数保留",
  "duplicate_policy": "先列出待确认"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "metric_definition": {
      "客单价": "销售净额除以有效订单数，退款订单口径待确认"
    },
    "checks_planned": [
      "订单ID重复",
      "门店字段缺失",
      "日期超出范围"
    ],
    "chart_plan": [
      {
        "metric": "销售额",
        "chart": "按周折线图"
      }
    ],
    "computed_values": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：清洗前后记录数及剔除原因可对账；指标计算可重跑且不是模型心算的最终数值；图表单位、分母、日期和缺失值说明完整；相关关系不直接写成因果结论。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
